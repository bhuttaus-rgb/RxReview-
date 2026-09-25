from data.salgado_quiz import SALGADO_QUESTIONS, QUESTIONS_BY_ID, shuffled_questions


def test_question_bank_has_37_unique_questions():
    assert len(SALGADO_QUESTIONS) == 37
    assert len(QUESTIONS_BY_ID) == 37
    assert len({question.id for question in SALGADO_QUESTIONS}) == 37


def test_every_question_has_valid_choices_and_feedback():
    for question in SALGADO_QUESTIONS:
        assert len(question.choices) == 4
        assert len(question.correct) == 1
        assert 0 <= question.correct[0] < len(question.choices)
        assert question.prompt.strip()
        assert question.explanation.strip()
        assert question.memory_hook.strip()


def test_retakes_shuffle_without_losing_questions():
    first = shuffled_questions(301)
    second = shuffled_questions(302)
    assert first != second
    assert set(first) == set(second) == set(SALGADO_QUESTIONS)
