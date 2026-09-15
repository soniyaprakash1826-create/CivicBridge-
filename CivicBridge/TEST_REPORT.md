# CivicBridge test report

Date: 2026-09-01

## Automated checks completed
- Python compileall: PASS
- Scheme API normalization: PASS
- Supported JSON response shapes: PASS
- SQLite API cache/sync: PASS
- Central + state filtering (Maharashtra/Karnataka): PASS
- End-to-end local HTTP API -> normalization -> SQLite -> state filter: PASS
- Stale old live-catalogue template references removed: PASS

## Environment limitation
The test container did not have Flask installed and outbound package installation was unavailable, so a real Flask/browser smoke test could not be completed in this environment.

On the target computer, install the requirements and run:
`pip install -r requirements.txt`
`python app.py`
Then open `http://127.0.0.1:5050`.

## API note
The project is API-integrated but requires a real API endpoint/resource ID and credentials (if required) in `.env`. No secret API key is included in this ZIP.
