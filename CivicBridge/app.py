import sqlite3
import uuid
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, g, render_template, request, redirect, url_for, abort

from benefits_data import evaluate_all, get_program, PROGRAMS
from scheme_api import init_api_table, sync_api_schemes, get_api_schemes
from central_schemes_catalogue import CENTRAL_SCHEMES_CATALOGUE, get_categories, get_catalogue

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env')
DB_PATH = BASE_DIR / "civicbridge.db"

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_last_sync(db):
    init_api_table(db)
    row = db.execute("SELECT MAX(synced_at) AS t FROM api_schemes").fetchone()
    return row["t"] if row and row["t"] else None


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id TEXT PRIMARY KEY,
            household_size INTEGER,
            income REAL,
            caste TEXT,
            age INTEGER,
            disability INTEGER,
            veteran INTEGER,
            employed INTEGER,
            recent_job_loss INTEGER,
            has_young_child_or_pregnant INTEGER,
            farmer INTEGER DEFAULT 0,
            urban INTEGER DEFAULT 0,
            female_applicant INTEGER DEFAULT 0,
            street_vendor INTEGER DEFAULT 0,
            business INTEGER DEFAULT 0,
            widow INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS doc_status (
            case_id TEXT,
            program_id TEXT,
            doc_name TEXT,
            checked INTEGER DEFAULT 0,
            PRIMARY KEY (case_id, program_id, doc_name)
        );
        """
    )
    init_api_table(db)
    db.commit()
    db.close()


@app.route("/schemes")
def schemes_catalogue():
    category = request.args.get("category", "").strip()
    db = get_db()
    init_api_table(db)
    return render_template(
        "schemes.html",
        category=category,
        categories=get_categories(),
        catalogue=get_catalogue(category),
        live_schemes=get_api_schemes(db),
        last_sync=get_last_sync(db),
    )

@app.route("/", methods=["GET"])
def index():
    db = get_db()
    init_api_table(db)
    live_count = db.execute("SELECT COUNT(*) AS n FROM api_schemes").fetchone()["n"]
    return render_template(
        "index.html", live_count=live_count, last_sync=get_last_sync(db),
        catalogue_count=len(CENTRAL_SCHEMES_CATALOGUE),
    )


@app.route("/sync-schemes", methods=["POST"])
def sync_schemes():
    db = get_db()
    try:
        result = sync_api_schemes(db)
        return render_template("sync_result.html", ok=True, result=result, last_sync=get_last_sync(db))
    except Exception as exc:
        return render_template("sync_result.html", ok=False, error=str(exc), last_sync=get_last_sync(db)), 502


@app.route("/results", methods=["POST"])
def submit_intake():
    f = request.form
    profile = {
        "household_size": int(f.get("household_size", 1)),
        "income": float(f.get("income", 0)),
        "caste": f.get("caste", "").strip() or "Other/Prefer not to say",
        "age": int(f.get("age", 0)),
        "disability": 1 if f.get("disability") == "yes" else 0,
        "veteran": 1 if f.get("veteran") == "yes" else 0,
        "employed": 1 if f.get("employed") == "yes" else 0,
        "recent_job_loss": 1 if f.get("recent_job_loss") == "yes" else 0,
        "has_young_child_or_pregnant": 1 if f.get("has_young_child_or_pregnant") == "yes" else 0,
        "farmer": 1 if f.get("farmer") == "yes" else 0,
        "urban": 1 if f.get("urban") == "yes" else 0,
        "female_applicant": 1 if f.get("female_applicant") == "yes" else 0,
        "street_vendor": 1 if f.get("street_vendor") == "yes" else 0,
        "business": 1 if f.get("business") == "yes" else 0,
        "widow": 1 if f.get("widow") == "yes" else 0,
    }

    case_id = str(uuid.uuid4())[:8]
    db = get_db()
    db.execute(
        """INSERT INTO cases
           (id, household_size, income, caste, age, disability, veteran,
            employed, recent_job_loss, has_young_child_or_pregnant, farmer, urban,
            female_applicant, street_vendor, business, widow)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (case_id, profile["household_size"], profile["income"], profile["caste"],
         profile["age"], profile["disability"], profile["veteran"],
         profile["employed"], profile["recent_job_loss"], profile["has_young_child_or_pregnant"],
         profile["farmer"], profile["urban"], profile["female_applicant"],
         profile["street_vendor"], profile["business"], profile["widow"]),
    )
    db.commit()
    return redirect(url_for("results", case_id=case_id))


def load_profile(case_id):
    db = get_db()
    row = db.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()
    if row is None:
        abort(404)
    return dict(row)


@app.route("/results/<case_id>")
def results(case_id):
    profile = load_profile(case_id)
    matches = evaluate_all(profile)
    eligible_count = sum(1 for m in matches if m["eligible"])
    db = get_db()
    init_api_table(db)
    api_schemes = get_api_schemes(db)
    return render_template(
        "results.html", case_id=case_id, profile=profile,
        matches=matches, eligible_count=eligible_count, api_schemes=api_schemes,
        last_sync=get_last_sync(db),
    )


@app.route("/checklist/<case_id>/<program_id>")
def checklist(case_id, program_id):
    profile = load_profile(case_id)
    program = get_program(program_id)
    if program is None:
        abort(404)

    db = get_db()
    checked_rows = db.execute(
        "SELECT doc_name, checked FROM doc_status WHERE case_id = ? AND program_id = ?",
        (case_id, program_id),
    ).fetchall()
    checked_map = {r["doc_name"]: r["checked"] for r in checked_rows}

    docs = [{"name": d, "checked": bool(checked_map.get(d, 0))} for d in program["documents"]]
    done = sum(1 for d in docs if d["checked"])
    readiness_pct = int((done / len(docs)) * 100) if docs else 0

    eligible, reason = program["eligibility"](profile)

    return render_template(
        "checklist.html", case_id=case_id, program=program, docs=docs,
        readiness_pct=readiness_pct, eligible=eligible, reason=reason,
    )


@app.route("/checklist/<case_id>/<program_id>/toggle", methods=["POST"])
def toggle_doc(case_id, program_id):
    doc_name = request.form["doc_name"]
    checked = 1 if request.form.get("checked") == "true" else 0
    db = get_db()
    db.execute(
        """INSERT INTO doc_status (case_id, program_id, doc_name, checked)
           VALUES (?, ?, ?, ?)
           ON CONFLICT(case_id, program_id, doc_name)
           DO UPDATE SET checked = excluded.checked""",
        (case_id, program_id, doc_name, checked),
    )
    db.commit()
    return redirect(url_for("checklist", case_id=case_id, program_id=program_id))


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5050)
