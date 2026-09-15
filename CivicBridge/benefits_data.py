"""
CivicBridge — India government schemes.

The schemes below are Indian government programmes verified against official
Government of India portals during September 2026. This is a screening/
discovery prototype, NOT an official eligibility determination.

Important: many Indian schemes have detailed household, land, social-category,
age, occupation and other conditions. The checks here are deliberately
conservative and should always be confirmed on the linked official portal.

CivicBridge screens Central Government schemes only. profile["caste"] is
expected to be one of "General", "OBC", "SC", "ST", "EWS" or "Other/Prefer
not to say".

For the much larger browsable list of Central Government schemes (without
personalised eligibility logic), see central_schemes_catalogue.py.
"""

PROGRAMS = [
    {
        "id": "pm-kisan",
        "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
        "desc": "Income support for eligible land-holding farmer families. The official portal states that eligible families receive ₹6,000 per year in three equal instalments, subject to exclusions.",
        "category": "Agriculture",
        "eligibility": lambda p: (
            (p["farmer"], "You indicated that you are a farmer. PM-KISAN eligibility also depends on landholding and scheme exclusion criteria."),
            (False, "PM-KISAN is intended for eligible land-holding farmer families; indicate that you are a farmer to screen this scheme.")
        )[1 if not p["farmer"] else 0],
        "documents": ["Aadhaar/details required by the official registration process", "Landholding/land-record details", "Bank account details", "Mobile number"],
        "rejection_reasons": ["Applicant does not satisfy the landholding or family definition", "Applicant falls under an exclusion category", "Required eKYC or verification is incomplete"],
        "apply_note": "Use the official PM-KISAN portal to register, check status and complete eKYC.",
        "official_url": "https://pmkisan.gov.in/",
    },
    {
        "id": "pm-jay",
        "name": "Ayushman Bharat PM-JAY",
        "desc": "Government health assurance scheme providing eligible beneficiaries access to cashless treatment at empanelled hospitals, subject to scheme rules and state implementation.",
        "category": "Health",
        "eligibility": lambda p: (
            (p["income"] <= 300000, "Your reported annual household income is within a broad screening range. Actual PM-JAY eligibility is determined through the official beneficiary database and applicable rules."),
            (False, "Your reported income is above this prototype's screening range. Actual PM-JAY eligibility is determined through the official beneficiary database and applicable rules.")
        )[1 if p["income"] > 300000 else 0],
        "documents": ["Aadhaar or another accepted identity document", "Mobile number", "Beneficiary/family details required by the official portal"],
        "rejection_reasons": ["Applicant/family is not found eligible in the official beneficiary database", "Identity or beneficiary details cannot be verified"],
        "apply_note": "Check beneficiary eligibility through the official National Health Authority/PM-JAY services.",
        "official_url": "https://pmjay.gov.in/",
    },
    {
        "id": "pmay-u2",
        "name": "PMAY-U 2.0 (Pradhan Mantri Awas Yojana – Urban 2.0)",
        "desc": "Housing assistance for eligible urban poor and middle-income families through the PMAY-U 2.0 mission.",
        "category": "Housing",
        "eligibility": lambda p: (
            (p["urban"], "You indicated an urban residence. PMAY-U 2.0 has additional conditions, including household income category and housing ownership requirements."),
            (False, "This prototype screens PMAY-U 2.0 for users who indicate an urban residence.")
        )[1 if not p["urban"] else 0],
        "documents": ["Identity proof", "Address/residence proof", "Income proof", "Bank account details", "Property/house details where applicable"],
        "rejection_reasons": ["Household does not meet the applicable income/ownership conditions", "Application or property details cannot be verified", "Duplicate or incompatible housing benefit already exists"],
        "apply_note": "Use the official Government of India PMAY-U 2.0 application/service page and follow the applicable urban local body process.",
        "official_url": "https://www.india.gov.in/services/details/apply-for-housing-assistance-under-pradhan-mantri-awas-yojana-urban-20",
    },
    {
        "id": "pmuy",
        "name": "Pradhan Mantri Ujjwala Yojana (PMUY)",
        "desc": "LPG connection support for eligible households, with eligibility conditions defined by the scheme.",
        "category": "Energy",
        "eligibility": lambda p: (
            (p["female_applicant"] and p["income"] <= 300000, "You indicated a female applicant and a household income within this prototype's screening range. Final eligibility is determined by PMUY rules and household verification."),
            (False, "This prototype screens PMUY when a female applicant is indicated and household income is within the screening range.")
        )[1 if not (p["female_applicant"] and p["income"] <= 300000) else 0],
        "documents": ["Aadhaar/accepted identity proof", "Address proof", "Bank account details", "Household/family details required by the LPG distributor"],
        "rejection_reasons": ["Household already has an LPG connection where prohibited", "Required identity/address details cannot be verified", "Applicant does not meet the scheme's household eligibility conditions"],
        "apply_note": "Use the official Government of India Ujjwala information/application service or an authorised LPG distributor.",
        "official_url": "https://www.india.gov.in/category/housing-local-services/subcategory/electricity-lpg-water/details/pradhan-mantri-ujjwala-yojana-pmuy",
    },
    {
        "id": "pm-svanidhi",
        "name": "PM SVANidhi",
        "desc": "Micro-credit support for eligible street vendors, implemented under the Government of India's street-vendor livelihood programme.",
        "category": "Self-employment",
        "eligibility": lambda p: (
            (p["street_vendor"], "You indicated that you are a street vendor. The official scheme has additional vendor/certificate and lending conditions."),
            (False, "PM SVANidhi is intended for eligible street vendors; indicate that you are a street vendor to screen this scheme.")
        )[1 if not p["street_vendor"] else 0],
        "documents": ["Identity proof", "Street-vendor/certificate or survey details as applicable", "Mobile number", "Bank account details"],
        "rejection_reasons": ["Vendor details are not found or cannot be verified", "Required identification/certificate information is missing", "Application does not meet the lending conditions"],
        "apply_note": "Follow the official PM SVANidhi application process through the Government of India/participating lending ecosystem.",
        "official_url": "https://www.india.gov.in/category/money-taxes/subcategory/banking-insurance/details/prime-minister-street-vendors-atmanirbhar-nidhi-pm-svanidhi",
    },
    {
        "id": "pmjd-y",
        "name": "Pradhan Mantri Jan-Dhan Yojana (PMJDY)",
        "desc": "Financial inclusion programme providing access to banking, savings/deposit accounts, remittance, credit, insurance and pension services.",
        "category": "Banking",
        "eligibility": lambda p: (True, "PMJDY is a financial-inclusion programme. Account opening and benefits depend on the applicable bank and scheme rules."),
        "documents": ["Accepted identity/KYC document", "Address details", "Mobile number where applicable", "Other KYC information requested by the bank"],
        "rejection_reasons": ["KYC documents are incomplete or cannot be verified", "Bank-specific account-opening requirements are not satisfied"],
        "apply_note": "Visit a participating bank or use the official PMJDY information and account-opening resources.",
        "official_url": "https://www.india.gov.in/services/details/pradhan-mantri-jan-dhan-yojana-pmjdy",
    },
    {
        "id": "pmmy",
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "desc": "Credit support for eligible non-corporate, non-farming micro and small enterprises.",
        "category": "Business",
        "eligibility": lambda p: (
            (p["business"], "You indicated that you run a business/self-employment activity. Loan approval is subject to the lender's assessment and PMMY conditions."),
            (False, "PMMY is intended for eligible micro/small business activity; indicate business/self-employment to screen this scheme.")
        )[1 if not p["business"] else 0],
        "documents": ["Identity/KYC documents", "Address proof", "Business/activity details", "Bank account details", "Documents requested by the lending institution"],
        "rejection_reasons": ["Business/activity is outside applicable PMMY scope", "KYC or business documents are incomplete", "Lender's credit assessment is not satisfied"],
        "apply_note": "Apply through an eligible lending institution and confirm the current loan category/conditions.",
        "official_url": "https://www.india.gov.in/category/justice-law-grievances/subcategory/institutions-organizations/details/pradhan-mantri-mudra-yojana-pmmy-in-business-activity-loan",
    },
    {
        "id": "nsap",
        "name": "National Social Assistance Programme (NSAP)",
        "desc": "Social security assistance covering programmes for eligible older persons, widows, persons with disabilities and bereaved families, with detailed conditions.",
        "category": "Social Security",
        "eligibility": lambda p: (
            (p["age"] >= 60 or p["widow"] or p["disability"], "You indicated an age/household circumstance that may fit an NSAP component. Exact eligibility depends on the relevant component and applicable state/central rules."),
            (False, "This prototype screens NSAP for older applicants, widows or applicants indicating disability; exact component eligibility must be verified.")
        )[1 if not (p["age"] >= 60 or p["widow"] or p["disability"]) else 0],
        "documents": ["Identity proof", "Age proof where applicable", "Bank/post-office account details", "Disability/widowhood or other supporting documents where applicable"],
        "rejection_reasons": ["Applicant does not meet the applicable component's conditions", "Required supporting documents are missing", "State/local verification is incomplete"],
        "apply_note": "Check the official NSAP information and your state/local implementation process.",
        "official_url": "https://www.india.gov.in/category/business-self-employed/subcategory/career-information-jobs/details/information-on-national-social-assistance-programme-nsap",
    },
    {
        "id": "post-matric-scholarship",
        "name": "Post-Matric Scholarship (SC / ST / OBC)",
        "desc": "Central scholarship support for students from Scheduled Caste, Scheduled Tribe or Other Backward Class categories studying beyond matriculation, subject to income and course conditions.",
        "category": "Education",
        "eligibility": lambda p: (
            (p["caste"] in ("SC", "ST", "OBC"), "You indicated a social category (SC/ST/OBC) that this prototype screens for post-matric scholarship support. Exact eligibility also depends on income limits, course and state-level administration."),
            (False, "Post-Matric Scholarship is screened here for applicants who indicate SC, ST or OBC category; other applicants should check the National Scholarship Portal for schemes that may still apply to them.")
        )[1 if p["caste"] not in ("SC", "ST", "OBC") else 0],
        "documents": ["Caste/community certificate", "Income certificate", "Previous marksheet/admission proof", "Bank account details", "Aadhaar or accepted identity proof"],
        "rejection_reasons": ["Caste/community certificate is missing or not from a competent authority", "Household income exceeds the applicable ceiling", "Application not renewed/verified each academic year"],
        "apply_note": "Apply and renew every year through the National Scholarship Portal (scholarships.gov.in).",
        "official_url": "https://scholarships.gov.in/",
    },
    {
        "id": "pm-yasasvi",
        "name": "PM YASASVI Scholarship (OBC / EBC / DNT)",
        "desc": "Central scholarship for meritorious students from Other Backward Classes, Economically Backward Classes and De-notified/Nomadic Tribes at school and college level.",
        "category": "Education",
        "eligibility": lambda p: (
            (p["caste"] == "OBC", "You indicated OBC category, which this prototype screens for PM YASASVI. It also has an entrance-test/merit and income-ceiling requirement."),
            (False, "This prototype screens PM YASASVI for applicants who indicate OBC category; EBC/DNT applicants should check the National Scholarship Portal directly since this prototype does not separately collect that detail.")
        )[1 if p["caste"] != "OBC" else 0],
        "documents": ["Caste/community certificate", "Income certificate", "Previous academic records", "Bank account details"],
        "rejection_reasons": ["Entrance-test/merit cutoff not met", "Household income exceeds the applicable ceiling", "Required certificates are missing or unverified"],
        "apply_note": "Apply through the National Scholarship Portal (scholarships.gov.in) during the notified application window.",
        "official_url": "https://scholarships.gov.in/",
    },
    {
        "id": "stand-up-india",
        "name": "Stand-Up India Scheme",
        "desc": "Bank loans between ₹10 lakh and ₹1 crore to support at least one SC/ST borrower and one woman borrower per bank branch to set up a greenfield enterprise.",
        "category": "Business",
        "eligibility": lambda p: (
            (p["business"] and (p["caste"] in ("SC", "ST") or p["female_applicant"]), "You indicated a business/self-employment activity together with SC/ST category or a woman applicant, which this prototype screens for Stand-Up India. Bank appraisal and greenfield-enterprise conditions still apply."),
            (False, "Stand-Up India is screened here for applicants indicating business/self-employment activity together with SC/ST category or a woman applicant.")
        )[1 if not (p["business"] and (p["caste"] in ("SC", "ST") or p["female_applicant"])) else 0],
        "documents": ["Identity/KYC documents", "Caste/community certificate where applicable", "Business/project plan", "Address proof", "Bank account details"],
        "rejection_reasons": ["Enterprise is not a qualifying greenfield (new) venture", "Bank's credit appraisal is not satisfied", "Required category/identity documents are missing"],
        "apply_note": "Apply through the Stand-Up India portal or an eligible scheduled commercial bank branch.",
        "official_url": "https://www.standupmitra.in/",
    },
    {
        "id": "apy",
        "name": "Atal Pension Yojana (APY)",
        "desc": "Guaranteed minimum monthly pension scheme mainly for workers in the unorganised sector, with the pension amount depending on the contribution and joining age.",
        "category": "Social Security",
        "eligibility": lambda p: (
            (18 <= p["age"] <= 40, "Your indicated age falls within the APY enrolment window (18–40 years). A bank/post-office savings account and regular contribution are also required."),
            (False, "APY enrolment is open only to applicants aged 18 to 40; your indicated age falls outside this window.")
        )[1 if not (18 <= p["age"] <= 40) else 0],
        "documents": ["Bank or post-office savings account", "Aadhaar", "Mobile number", "Nominee details"],
        "rejection_reasons": ["Applicant is outside the 18–40 enrolment age window", "Applicant is already an income-tax payer (excluded from the government co-contribution period conditions)", "Auto-debit/contribution details are incomplete"],
        "apply_note": "Enrol through your bank or post office savings account, or via the APY/eNPS portal.",
        "official_url": "https://npscra.nsdl.co.in/scheme-details.php",
    },
]


def evaluate_all(profile):
    results = []
    for program in PROGRAMS:
        eligible, reason = program["eligibility"](profile)
        results.append({
            "id": program["id"], "name": program["name"], "desc": program["desc"],
            "category": program["category"], "eligible": eligible, "reason": reason,
            "documents": program["documents"], "rejection_reasons": program["rejection_reasons"],
            "apply_note": program["apply_note"], "official_url": program["official_url"],
        })
    results.sort(key=lambda r: not r["eligible"])
    return results


def get_program(program_id):
    return next((p for p in PROGRAMS if p["id"] == program_id), None)
