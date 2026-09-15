# CivicBridge 🇮🇳

### Bridging Citizens to Benefits by Eliminating Information Barriers and Paperwork Rejections

CivicBridge is a web-based application designed to help Indian citizens discover government welfare schemes they may be eligible for.

The application collects basic information about a citizen and their household, evaluates eligibility rules, and presents relevant government schemes along with eligibility information and required documents.

## 🎯 Objectives

- Help citizens discover relevant government welfare schemes.
- Simplify eligibility checking.
- Reduce confusion about required documents.
- Identify missing or incomplete documents.
- Reduce paperwork-related application rejections.
- Provide a simple and user-friendly interface for accessing scheme information.

## ✨ Features

- 🇮🇳 India-specific government welfare schemes
- 👤 Citizen profile-based eligibility checking
- 🏠 Household information evaluation
- 📋 Eligibility results
- 📄 Required document checklist
- ⚠️ Identification of missing documents
- 🏛️ Central and state-level scheme information
- 🔎 Simple and user-friendly interface
- 💾 SQLite database support
- 🌐 Flask-based web application

## 🛠️ Technologies Used

- **Python**
- **Flask**
- **SQLite**
- **HTML5**
- **CSS3**
- **JavaScript**
- **Jinja2**
- **Git & GitHub**

## 📂 Project Structure

```text
CivicBridge/
├── app.py
├── benefits_data.py
├── central_schemes_catalogue.py
├── scheme_api.py
├── civicbridge.db
├── requirements.txt
├── .env.example
├── API_SETUP.md
├── README_INDIA.md
├── TEST_REPORT.md
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── results.html
│   ├── schemes.html
│   └── checklist.html
└── static/
    ├── css/
    └── js/