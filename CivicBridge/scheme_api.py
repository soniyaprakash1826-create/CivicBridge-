"""
CivicBridge scheme API integration.

Primary integration:
- Generic SCHEME_API_URL for a dedicated scheme API returning JSON.
- Optional Government of India's data.gov.in resource API.

Important:
myScheme is the Government of India's national scheme discovery platform,
but it does not expose a documented public scheme-catalogue API on its public
site. Therefore CivicBridge does NOT pretend that a private/internal myScheme
endpoint is a public API.

CivicBridge is Central Government schemes only. Any state-level records a
configured source may still return are normalized (so "level" is tracked)
but are filtered out by filter_central_only()/get_api_schemes() before they
reach the UI.

Configure an actual API in .env:
    SCHEME_API_URL=https://your-api.example/schemes
or data.gov.in:
    DATA_GOV_API_KEY=your_key
    DATA_GOV_RESOURCE_IDS=resource-id-1,resource-id-2

The provider normalizes records into CivicBridge's common scheme format.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone
from typing import Any
import requests

INDIA_STATES = {
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
    "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
    "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
    "Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands",
    "Chandigarh","Dadra and Nagar Haveli and Daman and Diu","Delhi",
    "Jammu and Kashmir","Ladakh","Lakshadweep","Puducherry",
}

CENTRAL_LABELS = {
    "central", "central government", "government of india", "goi",
    "union government", "ministry of india"
}


def _first(record: dict, names: list[str], default=""):
    lowered = {str(k).lower().replace("-", "_").replace(" ", "_"): v for k, v in record.items()}
    for name in names:
        key = name.lower().replace("-", "_").replace(" ", "_")
        if key in lowered and lowered[key] not in (None, ""):
            return lowered[key]
    return default


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    if not text:
        return []
    return [x.strip() for x in text.replace("|", ",").split(",") if x.strip()]


def normalize(record: dict, source: str) -> dict | None:
    name = _first(record, ["name", "scheme_name", "title", "scheme"])
    if not name:
        return None

    state_value = _first(record, [
        "state", "states", "state_ut", "state_ut_name", "jurisdiction",
        "applicable_state", "applicable_states"
    ])
    ministry = _first(record, ["ministry", "department", "agency", "implementing_department"])
    level = _first(record, ["level", "government_level", "scheme_level"])

    states = _as_list(state_value)
    if not states:
        # Some APIs put the state in jurisdiction text.
        states = [s for s in INDIA_STATES if s.lower() in str(record).lower()]

    is_central = (
        str(level).strip().lower() in CENTRAL_LABELS
        or str(ministry).strip().lower() in CENTRAL_LABELS
        or not states
    )

    url = _first(record, [
        "official_url", "application_url", "apply_url", "url", "link", "scheme_url"
    ])

    return {
        "name": str(name).strip(),
        "description": str(_first(record, ["description", "details", "benefits", "summary"], "")).strip()[:2000],
        "category": str(_first(record, ["category", "sector", "theme"], "Government scheme")).strip(),
        "ministry": str(ministry).strip(),
        "level": "Central Government" if is_central else "State Government",
        "states": states,
        "official_url": str(url).strip(),
        "source": source,
        "source_updated": str(_first(record, ["updated_on", "last_updated", "updated_at", "modified"], "")).strip(),
    }


def _json_records(payload: Any) -> list[dict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("records", "data", "results", "schemes", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


def fetch_custom_api() -> list[dict]:
    url = os.getenv("SCHEME_API_URL", "").strip()
    if not url:
        return []
    headers = {"Accept": "application/json", "User-Agent": "CivicBridge/2.0"}
    token = os.getenv("SCHEME_API_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return [normalize(r, "Configured scheme API") for r in _json_records(response.json())]


def fetch_data_gov() -> list[dict]:
    key = os.getenv("DATA_GOV_API_KEY", "").strip()
    ids = [x.strip() for x in os.getenv("DATA_GOV_RESOURCE_IDS", "").split(",") if x.strip()]
    if not key or not ids:
        return []

    records = []
    for resource_id in ids:
        url = f"https://api.data.gov.in/resource/{resource_id}"
        params = {"api-key": key, "format": "json", "limit": 1000}
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()
        for item in _json_records(payload):
            item = normalize(item, f"data.gov.in:{resource_id}")
            if item:
                records.append(item)
    return records


def fetch_all() -> list[dict]:
    # Prefer a dedicated scheme API; use data.gov.in as an additional source.
    result = []
    result.extend(fetch_custom_api())
    result.extend(fetch_data_gov())

    unique = {}
    for item in result:
        key = (item["name"].lower(), item["level"], tuple(sorted(item["states"])))
        unique[key] = item
    return list(unique.values())


def filter_central_only(schemes: list[dict]) -> list[dict]:
    """CivicBridge is Central Government schemes only — state schemes from a
    synced source are intentionally excluded from what's shown to users."""
    return [s for s in schemes if s["level"] == "Central Government"]


def init_api_table(db: sqlite3.Connection):
    db.execute("""
        CREATE TABLE IF NOT EXISTS api_schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category TEXT,
            ministry TEXT,
            level TEXT,
            states TEXT,
            official_url TEXT,
            source TEXT,
            source_updated TEXT,
            synced_at TEXT NOT NULL,
            UNIQUE(name, level, states)
        )
    """)
    db.commit()


def sync_api_schemes(db: sqlite3.Connection) -> dict:
    init_api_table(db)
    records = fetch_all()
    now = datetime.now(timezone.utc).isoformat()

    for s in records:
        db.execute("""
            INSERT INTO api_schemes
            (name, description, category, ministry, level, states,
             official_url, source, source_updated, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name, level, states) DO UPDATE SET
              description=excluded.description,
              category=excluded.category,
              ministry=excluded.ministry,
              official_url=excluded.official_url,
              source=excluded.source,
              source_updated=excluded.source_updated,
              synced_at=excluded.synced_at
        """, (
            s["name"], s["description"], s["category"], s["ministry"], s["level"],
            "|".join(s["states"]), s["official_url"], s["source"],
            s["source_updated"], now
        ))
    db.commit()
    return {"fetched": len(records), "synced_at": now}


def get_api_schemes(db):
    init_api_table(db)
    rows = db.execute("SELECT * FROM api_schemes ORDER BY name").fetchall()
    result = []
    for r in rows:
        states = [x for x in (r["states"] or "").split("|") if x]
        item = dict(r)
        item["states"] = states
        result.append(item)
    return filter_central_only(result)
