from dataclasses import dataclass
from data.cases import ClinicalCase

@dataclass(frozen=True)
class MedicationScore:
    medication_id: str
    decision_points: int
    modification_points: int
    @property
    def total(self) -> int:
        return self.decision_points + self.modification_points

def score_case(case: ClinicalCase, answers: dict[str, dict[str, str | None]]) -> tuple[int, list[MedicationScore]]:
    """Score out of 100. MODIFY awards 15 points for the decision plus 5 for the detail."""
    results = []
    for med in case.medications:
        answer = answers.get(med.id, {})
        correct = answer.get("decision") == med.accepted_decision
        decision_points = (15 if med.accepted_decision == "MODIFY" else 20) if correct else 0
        modification_points = 5 if correct and med.accepted_decision == "MODIFY" and answer.get("modification") == med.accepted_modification else 0
        results.append(MedicationScore(med.id, decision_points, modification_points))
    return sum(result.total for result in results), results

def xp_earned(case: ClinicalCase, answers: dict[str, dict[str, str | None]]) -> int:
    correct = sum(
        answers.get(med.id, {}).get("decision") == med.accepted_decision
        and (med.accepted_decision != "MODIFY" or answers.get(med.id, {}).get("modification") == med.accepted_modification)
        for med in case.medications
    )
    return 30 + correct * 10 + (20 if correct == len(case.medications) else 0)
