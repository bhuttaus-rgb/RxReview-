from collections import Counter
import re

from data.id_quiz import ID_QUIZ_01, LEARNING_SEQUENCE, QUESTIONS_BY_ID, STARRED_BRAND_PAIRS, display_choices, display_questions, questions_for_stage, simulation_questions


def test_question_bank_has_unique_ids_and_expected_size():
    assert len(ID_QUIZ_01) == 87
    assert len(QUESTIONS_BY_ID) == len(ID_QUIZ_01)


def test_every_question_has_four_unique_choices_and_one_locked_answer():
    for question in ID_QUIZ_01:
        assert len(question.choices) == 4
        assert len({choice.id for choice in question.choices}) == 4
        assert len({choice.text for choice in question.choices}) == 4
        assert sum(choice.id == question.correct_choice_id for choice in question.choices) == 1
        assert all(choice.feedback.strip() for choice in question.choices)
        assert question.explanation.strip()
        assert question.memory_hook.strip()
        assert question.source_title.strip()
        assert question.source_section.strip()


def test_learning_sequence_and_stage_distribution_are_balanced():
    expected_stages = [stage.id for stage in LEARNING_SEQUENCE]
    counts = Counter(question.stage for question in ID_QUIZ_01)
    assert expected_stages == ["identify", "classify", "mechanism", "cover", "brand"]
    assert counts == {"identify": 12, "classify": 12, "mechanism": 12, "cover": 12, "brand": 39}
    assert all(questions_for_stage(stage) for stage in expected_stages)


def test_starred_top_250_data_is_complete_and_only_testable_pairs_generate_questions():
    assert len(STARRED_BRAND_PAIRS) == 42
    assert sum(bool(brands) for _, brands in STARRED_BRAND_PAIRS) == 39
    assert {generic for generic, brands in STARRED_BRAND_PAIRS if not brands} == {
        "Penicillin G procaine", "Ceftriaxone", "Gentamicin"
    }


def test_quiz_does_not_introduce_dose_testing():
    dose_pattern = re.compile(r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g)\b|\bevery\s+\d+\s+hours?\b|\b(?:once|twice)\s+daily\b")
    for question in ID_QUIZ_01:
        assessed_text = " ".join([question.prompt, *(choice.text for choice in question.choices)]).lower()
        assert not dose_pattern.search(assessed_text)


def test_quiz_does_not_test_routes_of_administration():
    route_pattern = re.compile(r"\b(?:route|oral|intravenous|intramuscular|topical|inhaled|iv|po|im)\b")
    for question in ID_QUIZ_01:
        assessed_text = " ".join([
            question.topic,
            question.prompt,
            *(choice.text for choice in question.choices),
            *(choice.feedback for choice in question.choices),
            question.explanation,
            question.memory_hook,
            *question.tags,
        ]).lower()
        assert not route_pattern.search(assessed_text)


def test_display_order_is_stable_and_correct_answers_are_distributed():
    correct_positions = []
    for question in ID_QUIZ_01:
        first_order = display_choices(question, attempt_seed=101)
        assert first_order == display_choices(question, attempt_seed=101)
        assert set(first_order) == set(question.choices)
        correct_positions.append(next(index for index, choice in enumerate(first_order) if choice.id == question.correct_choice_id))
    assert len(set(correct_positions)) == 4


def test_display_order_can_change_between_attempts():
    question = ID_QUIZ_01[0]
    orders = {
        tuple(choice.id for choice in display_choices(question, attempt_seed=seed))
        for seed in range(20)
    }
    assert len(orders) > 1


def test_question_order_is_stable_and_preserves_learning_stage_sequence():
    first_order = display_questions(attempt_seed=101)
    assert first_order == display_questions(attempt_seed=101)
    assert set(first_order) == set(ID_QUIZ_01)
    assert [question.stage for question in first_order] == [
        stage.id for stage in LEARNING_SEQUENCE
        for _ in questions_for_stage(stage.id)
    ]


def test_question_order_changes_between_attempts():
    orders = {
        tuple(question.id for question in display_questions(attempt_seed=seed))
        for seed in range(20)
    }
    assert len(orders) > 1


def test_simulation_draws_60_balanced_shuffled_questions():
    simulation = simulation_questions(attempt_seed=101)
    assert len(simulation) == 60
    assert Counter(question.stage for question in simulation) == {
        "identify": 12, "classify": 12, "mechanism": 12, "cover": 12, "brand": 12
    }
    assert len({question.id for question in simulation}) == 60
    assert simulation == simulation_questions(attempt_seed=101)
    assert simulation != simulation_questions(attempt_seed=102)
