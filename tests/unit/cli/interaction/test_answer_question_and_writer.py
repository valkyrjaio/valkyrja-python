#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for Answer, Question, Progress, the QuestionWriter, and the config."""

from typing import Any

import pytest

from tests.fixtures.cli.interaction.recording_question_fixture import (
    RecordingQuestionFixture,
    pass_through,
)
from valkyrja.cli.interaction.data.cli_interaction_config import CliInteractionConfig
from valkyrja.cli.interaction.message.answer import Answer
from valkyrja.cli.interaction.message.contract.question_contract import QuestionContract
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.progress import Progress
from valkyrja.cli.interaction.message.question import Question
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.output import Output
from valkyrja.cli.interaction.throwable.exception.cli_interaction_expected_question_output_exception import (
    CliInteractionExpectedQuestionOutputException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_validation_callable_exception import (
    CliInteractionNoValidationCallableException,
)
from valkyrja.cli.interaction.writer.question_writer import QuestionWriter


def test_an_answer_starts_at_the_default_response() -> None:
    answer = Answer("yes")

    assert answer.get_default_response() == "yes"
    assert answer.get_user_response() == "yes"
    assert answer.get_allowed_responses() == ["yes"]
    assert not answer.has_been_answered()


def test_an_answer_adds_the_default_to_the_allowed_responses() -> None:
    answer = Answer("yes", allowed_responses=["no"])

    assert answer.get_allowed_responses() == ["no", "yes"]


def test_an_answer_keeps_an_allowed_list_that_holds_the_default() -> None:
    answer = Answer("yes", allowed_responses=["yes", "no"])

    assert answer.get_allowed_responses() == ["yes", "no"]


def test_the_text_of_an_answer_holds_the_response() -> None:
    assert Answer("yes").get_text() == "You answered: `yes`"


def test_with_default_response_moves_the_user_response_when_unanswered() -> None:
    answer = Answer("yes")

    changed = answer.with_default_response("no")

    assert changed.get_user_response() == "no"
    assert changed.get_allowed_responses() == ["yes", "no"]
    assert answer.get_default_response() == "yes"


def test_with_default_response_keeps_the_user_response_once_answered() -> None:
    answer = Answer("yes", has_been_answered=True).with_user_response("maybe")

    changed = answer.with_default_response("no")

    assert changed.get_user_response() == "maybe"


def test_with_default_response_keeps_an_allowed_list_that_holds_it() -> None:
    answer = Answer("yes", allowed_responses=["yes", "no"])

    assert answer.with_default_response("no").get_allowed_responses() == ["yes", "no"]


def test_with_allowed_responses_replaces_the_list() -> None:
    answer = Answer("yes")

    changed = answer.with_allowed_responses("a", "b")

    assert changed.get_allowed_responses() == ["a", "b", "yes"]


def test_with_allowed_responses_keeps_a_list_that_holds_the_default() -> None:
    assert Answer("yes").with_allowed_responses("yes", "no").get_allowed_responses() == ["yes", "no"]


def test_get_allowed_responses_copies_the_list() -> None:
    answer = Answer("yes")

    answer.get_allowed_responses().clear()

    assert answer.get_allowed_responses() == ["yes"]


def test_with_user_response_and_with_has_been_answered_return_copies() -> None:
    answer = Answer("yes")

    assert answer.with_user_response("no").get_user_response() == "no"
    assert answer.with_has_been_answered(True).has_been_answered()
    assert answer.get_user_response() == "yes"
    assert not answer.has_been_answered()


def test_an_answer_without_a_validator_raises_when_asked_for_one() -> None:
    with pytest.raises(CliInteractionNoValidationCallableException, match="No validation callable"):
        Answer("yes").get_validation_callable()


def test_an_answer_carries_a_validator() -> None:
    answer = Answer("yes", validation_callable=lambda response: response == "ok")

    assert answer.has_validation_callable()
    assert answer.get_validation_callable()("ok")


def test_with_validation_callable_returns_a_copy() -> None:
    answer = Answer("yes")

    changed = answer.with_validation_callable(lambda response: True)

    assert changed.has_validation_callable()
    assert not answer.has_validation_callable()


def test_without_validation_callable_returns_a_copy() -> None:
    answer = Answer("yes", validation_callable=lambda response: True)

    changed = answer.without_validation_callable()

    assert not changed.has_validation_callable()
    assert answer.has_validation_callable()


def test_a_response_in_the_allowed_list_is_valid() -> None:
    assert Answer("yes").is_valid_response()


def test_a_response_outside_the_allowed_list_is_not_valid() -> None:
    assert not Answer("yes").with_user_response("maybe").is_valid_response()


def test_a_validator_accepts_a_response_outside_the_allowed_list() -> None:
    answer = Answer("yes", validation_callable=lambda response: response == "maybe")

    assert answer.with_user_response("maybe").is_valid_response()


def test_a_validator_rejects_a_response_outside_the_allowed_list() -> None:
    answer = Answer("yes", validation_callable=lambda response: False)

    assert not answer.with_user_response("maybe").is_valid_response()


def test_a_progress_holds_its_state() -> None:
    progress = Progress("working", is_complete=True, percentage=50)

    assert progress.is_complete()
    assert progress.get_percentage() == 50
    assert progress.get_text() == "working"


def test_the_progress_setters_return_copies() -> None:
    progress = Progress("working")

    assert progress.with_is_complete(True).is_complete()
    assert progress.with_percentage(10).get_percentage() == 10
    assert not progress.is_complete()
    assert progress.get_percentage() == 0


def test_a_question_holds_its_answer_and_callback() -> None:
    answer = Answer("yes")
    question = RecordingQuestionFixture("Continue?", answer)

    assert question.get_answer() is answer
    assert question.has_formatter()
    assert callable(question.get_callable())


def test_the_question_setters_return_copies() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"))
    other = Answer("no")

    assert question.with_answer(other).get_answer() is other
    assert question.with_callable(lambda output, answer: output) is not question
    assert question.get_answer() is not other


def test_ask_reads_the_response_and_marks_the_answer() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), ["no"])

    answered = question.ask()

    assert answered.get_user_response() == "no"
    assert answered.has_been_answered()


def test_ask_with_an_empty_response_keeps_the_default() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), [""])

    answered = question.ask()

    assert answered.get_user_response() == "yes"
    assert answered.has_been_answered()


def test_the_writer_takes_a_question_alone() -> None:
    writer = QuestionWriter()

    assert writer.should_write_message(RecordingQuestionFixture("Q", Answer("yes")))
    assert not writer.should_write_message(Message("plain"))


def test_the_writer_rejects_a_message_that_is_no_question() -> None:
    with pytest.raises(CliInteractionExpectedQuestionOutputException, match="only questions"):
        QuestionWriter().write(EmptyOutput(), Message("plain"))


def test_the_writer_asks_and_writes_the_answer() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes", allowed_responses=["no"]), ["no"])

    output = QuestionWriter().write(EmptyOutput(), question)

    assert question.reads == 1
    assert output.has_written_message()


def test_the_writer_does_not_ask_a_output_that_is_not_interactive() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), ["no"])

    QuestionWriter().write(EmptyOutput(is_interactive=False), question)

    assert question.reads == 0


def test_the_writer_does_not_ask_a_quiet_output() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), ["no"])

    QuestionWriter().write(EmptyOutput(is_quiet=True), question)

    assert question.reads == 0


def test_the_writer_does_not_ask_a_silent_output() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), ["no"])

    QuestionWriter().write(EmptyOutput(is_silent=True), question)

    assert question.reads == 0


def test_the_writer_asks_again_after_an_invalid_response() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes", allowed_responses=["no"]), ["maybe", "no"])

    QuestionWriter().write(EmptyOutput(), question)

    assert question.reads == 2


def test_an_output_gives_a_question_to_the_writer() -> None:
    question = RecordingQuestionFixture("Continue?", Answer("yes"), [""])
    output = EmptyOutput(True, False, False)

    written = output.with_added_message(question).write_messages()

    assert question.reads == 1
    assert written.has_written_message()


def test_the_config_holds_and_sets_each_flag() -> None:
    config = CliInteractionConfig()

    assert not config.is_quiet
    assert config.is_interactive
    assert not config.is_silent

    config.is_quiet = True
    config.is_interactive = False
    config.is_silent = True

    assert config.is_quiet
    assert not config.is_interactive
    assert config.is_silent


def test_the_config_takes_its_values() -> None:
    config = CliInteractionConfig(is_quiet=True, is_interactive=False, is_silent=True)

    assert config.is_quiet
    assert not config.is_interactive
    assert config.is_silent


def test_a_question_is_a_question_contract() -> None:
    assert isinstance(RecordingQuestionFixture("Q", Answer("yes")), QuestionContract)


def test_an_output_writes_a_plain_message_without_a_writer(capsys: Any) -> None:
    output = Output(True, False, False)

    output.with_added_message(Message("plain")).write_messages()

    assert capsys.readouterr().out == "plain"


def test_ask_reads_a_line_from_the_user(monkeypatch: pytest.MonkeyPatch) -> None:
    """The seam reads the terminal, so the test replaces the built-in `input`."""
    monkeypatch.setattr("builtins.input", lambda: "  no  ")
    question = Question("Continue?", pass_through, Answer("yes", allowed_responses=["no"]))

    assert question.ask().get_user_response() == "no"
