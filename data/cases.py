from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

Decision = Literal["KEEP", "MODIFY", "REMOVE"]

@dataclass(frozen=True)
class Reference:
    title: str
    section: str
    url: str

@dataclass(frozen=True)
class MedicationRule:
    id: str
    name: str
    dose: str
    indication: str
    accepted_decision: Decision
    rationale: str
    clinical_pearl: str
    reference: Reference
    modification_options: tuple[str, ...] = ()
    accepted_modification: str | None = None

@dataclass(frozen=True)
class ClinicalCase:
    id: str
    title: str
    difficulty: str
    patient: dict[str, str]
    vitals: dict[str, str]
    labs: dict[str, str]
    conditions: tuple[str, ...]
    risk_factors: tuple[str, ...]
    notes: tuple[str, ...]
    medications: tuple[MedicationRule, ...]

CASE_01 = ClinicalCase(
    id="case-01", title="Beginner Medication Review", difficulty="Foundational",
    patient={"name": "James R.", "age": "68 years", "sex": "Male", "reason": "Routine medication review", "allergies": "NKDA"},
    vitals={"BP": "148/86 mmHg", "HR": "72 bpm", "Weight": "84 kg", "BMI": "28.4 kg/m²"},
    labs={"A1c": "7.0%", "eGFR": "76 mL/min/1.73m²", "Potassium": "4.3 mEq/L", "LDL-C": "92 mg/dL"},
    conditions=("Hypertension", "Type 2 diabetes mellitus", "Hyperlipidemia", "GERD"),
    risk_factors=("Age >65", "Diabetes", "Hypertension", "Overweight"),
    notes=(
        "Reports good adherence, no new complaints, and no medication-related adverse effects.",
        "Office and home BP readings have remained 145–150/84–88 mmHg despite adherence.",
        "GERD symptoms recur when omeprazole is stopped and are controlled on the current dose.",
        "Atorvastatin 40 mg previously caused reproducible muscle symptoms; 20 mg is the maximum tolerated dose.",
        "Levothyroxine was accidentally carried forward from an old hospital list. James has never had hypothyroidism; pre-treatment TSH and chart review are normal.",
    ),
    medications=(
        MedicationRule("metformin", "Metformin", "500 mg twice daily", "Type 2 diabetes", "KEEP",
            "The medication has an active indication, is tolerated, and the A1c is reasonable. An eGFR of 76 does not require dose reduction or discontinuation.",
            "Always reassess kidney function when reviewing metformin.",
            Reference("ADA Standards of Care in Diabetes—2026", "Pharmacologic Approaches to Glycemic Treatment", "https://diabetesjournals.org/care/article/49/Supplement_1/S183/163934/9-Pharmacologic-Approaches-to-Glycemic-Treatment")),
        MedicationRule("atorvastatin", "Atorvastatin", "20 mg daily", "Cardiovascular risk reduction", "KEEP",
            "Statin therapy is indicated for this 68-year-old with diabetes. Because a higher dose caused reproducible muscle symptoms, 20 mg is his documented maximum tolerated dose.",
            "Evaluate statin therapy using age, diabetes, ASCVD risk, and tolerability—not LDL-C alone.",
            Reference("ADA Standards of Care in Diabetes—2026", "Cardiovascular Disease and Risk Management", "https://diabetesjournals.org/care/article/49/Supplement_1/S216/163933/10-Cardiovascular-Disease-and-Risk-Management")),
        MedicationRule("amlodipine", "Amlodipine", "5 mg daily", "Hypertension", "MODIFY",
            "Multiple home and office readings remain above goal despite adherence and tolerability. Increasing amlodipine to 10 mg daily is a reasonable next step for this case.",
            "Confirm the BP pattern, adherence, and tolerability before intensifying therapy—do not act on one isolated reading.",
            Reference("2025 ACC/AHA High Blood Pressure Guideline", "Treatment goal and medication management", "https://www.acc.org/Latest-in-Cardiology/Articles/2025/10/01/01/New-in-Clinical-Guidance-HBP"),
            ("Increase to amlodipine 10 mg daily", "Decrease to amlodipine 2.5 mg daily", "Change to amlodipine 5 mg twice daily"), "Increase to amlodipine 10 mg daily"),
        MedicationRule("omeprazole", "Omeprazole", "20 mg daily", "GERD", "KEEP",
            "GERD is documented, symptoms recur off therapy, and the lowest current dose controls symptoms without a relevant adverse effect.",
            "For maintenance PPI therapy, periodically confirm the indication and use the lowest effective dose.",
            Reference("ACG Clinical Guideline: GERD", "Maintenance proton pump inhibitor therapy", "https://gi.org/guidelines/")),
        MedicationRule("levothyroxine", "Levothyroxine", "50 mcg daily", "No valid indication documented", "REMOVE",
            "Medication reconciliation confirms this was carried forward in error. There is no thyroid diagnosis or abnormal pre-treatment TSH to justify continued therapy.",
            "Every medication needs a current indication; reconciliation errors can create avoidable harm and polypharmacy.",
            Reference("AHRQ MATCH Toolkit", "Medication reconciliation", "https://www.ahrq.gov/patient-safety/settings/hospital/match/index.html")),
    ),
)
CASES = {CASE_01.id: CASE_01}
