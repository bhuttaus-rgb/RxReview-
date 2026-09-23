from pathlib import Path

from data.khashan_quiz import KHASHAN_QUESTIONS, QUESTIONS_BY_ID, shuffled_questions


ASSET_DIR = Path(__file__).parents[1] / "assets" / "khashan"


def test_question_bank_has_30_unique_questions():
    assert len(KHASHAN_QUESTIONS) == 30
    assert len(QUESTIONS_BY_ID) == 30


def test_every_question_has_valid_answers_and_complete_feedback():
    for question in KHASHAN_QUESTIONS:
        assert 2 <= len(question.choices) <= 4
        assert question.correct
        assert all(0 <= index < len(question.choices) for index in question.correct)
        assert len(set(question.correct)) == len(question.correct)
        assert question.explanation.strip()
        assert question.memory_hook.strip()


def test_every_referenced_structure_asset_exists():
    for question in KHASHAN_QUESTIONS:
        for image_name in question.images:
            assert (ASSET_DIR / image_name).is_file(), f"Missing {image_name} for {question.id}"


def test_retakes_shuffle_question_order_without_losing_questions():
    first = shuffled_questions(101)
    second = shuffled_questions(102)
    assert first != second
    assert set(first) == set(second) == set(KHASHAN_QUESTIONS)
