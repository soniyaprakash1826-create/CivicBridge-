# CivicBridge API integration

CivicBridge no longer needs a hard-coded scheme list to display API-sourced
schemes.

## 1. Dedicated scheme API

Set:
`SCHEME_API_URL=https://...`

The endpoint should return JSON in one of these forms:
- `{"schemes": [...]}`
- `{"data": [...]}`
- `{"results": [...]}`
- or a raw JSON array.

Each scheme should ideally contain:
- `name` / `scheme_name`
- `description`
- `category`
- `state` or `states`
- `level` (`Central Government` or `State Government`)
- `official_url`
- `updated_on`

CivicBridge normalizes common field names automatically.

## 2. Government Open Data API

The Government of India's data.gov.in platform provides APIs for published
datasets. API access requires an API key. Configure:
`DATA_GOV_API_KEY`
and comma-separated `DATA_GOV_RESOURCE_IDS`.

Important: data.gov.in has APIs for individual published datasets; it is not
itself a single universal API containing every government scheme.

## 3. myScheme

myScheme is the official national scheme discovery platform and includes
Central and State/UT schemes, but its public site does not document a public
scheme-catalogue API. CivicBridge therefore does not scrape or call an
undocumented/private endpoint and claim that it is an API.

## Run

```bash
pip install -r requirements.txt
# copy .env.example to .env and set your API values
python app.py
```
