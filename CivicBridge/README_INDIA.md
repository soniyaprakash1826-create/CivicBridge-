# CivicBridge — India version

This version changes the original US-oriented prototype into an India-focused
government-scheme discovery prototype.

## Included schemes
- PM-KISAN
- Ayushman Bharat PM-JAY
- PMAY-U 2.0
- Pradhan Mantri Ujjwala Yojana
- PM SVANidhi
- PMJDY
- Pradhan Mantri MUDRA Yojana
- National Social Assistance Programme

Each scheme has an official Government of India source link.

## Important
The eligibility rules in this prototype are only screening rules. Indian
scheme eligibility can depend on detailed government databases, state rules,
income/category certificates, land records, household definitions and other
conditions. Users should verify the result on the official source before
applying.

## Run
```bash
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5050

If you already have an old `civicbridge.db`, delete it once before running
this version so SQLite creates the new schema.

## Live scheme updates

CivicBridge now has a **Refresh schemes now** button. It retrieves the public
scheme catalogue from **myScheme**, the Government of India's national scheme
discovery platform, and stores the latest successful result in SQLite.

The app keeps the previous catalogue if the official site is temporarily
unavailable. This is intentionally safer than deleting the existing data.

The eight schemes with detailed eligibility rules in `benefits_data.py` remain
screened by CivicBridge. Newly discovered schemes are displayed as live-source
entries with their official government source, but are **not automatically declared
eligible** because eligibility rules can be complex and can change. To add
precise screening for a new scheme, add its rules to `benefits_data.py`.


## API-based schemes
The current version uses `scheme_api.py`. Configure a dedicated scheme API or data.gov.in API credentials; there is no hard-coded scheme catalogue in the runtime path.
