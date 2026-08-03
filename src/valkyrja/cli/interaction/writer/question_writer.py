#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.formatter.highlighted_text_formatter import HighlightedTextFormatter
from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.contract.question_contract import QuestionContract
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.throwable.exception.cli_interaction_expected_question_output_exception import (
    CliInteractionExpectedQuestionOutputException,
)
from valkyrja.cli.interaction.writer.contract.writer_contract import WriterContract


class QuestionWriter(WriterContract):
    """Writes a question, reads the answer, and writes the answer back."""

    @override
    def should_write_message(self, message: MessageContract) -> bool:
        return isinstance(message, QuestionContract)

    @override
    def write(self, output: OutputContract, message: MessageContract) -> OutputContract:
        if not isinstance(message, QuestionContract):
            raise CliInteractionExpectedQuestionOutputException("This writer expects only questions")

        return self._ask_question(output, message)

    def _ask_question(self, output: OutputContract, question: QuestionContract) -> OutputContract:
        """Write the question, then read the answer when the output is interactive."""
        output = self._write_question(output, question)
        answer = question.get_answer()

        if output.is_interactive() and not output.is_quiet() and not output.is_silent():
            answer = question.ask()

            if not answer.is_valid_response():
                return self._ask_question(output, question.with_answer(answer))

        return self._write_answer_after_response(output, answer)

    def _write_question(self, output: OutputContract, question: QuestionContract) -> OutputContract:
        """Write the text of the question, with the allowed responses after it."""
        allowed = question.get_answer().get_allowed_responses()
        allowed_text = "/".join(allowed)

        return output.write_message(question.with_text(question.get_text())).write_message(
            Message(f" [{allowed_text}] ", HighlightedTextFormatter())
        )

    def _write_answer_after_response(self, output: OutputContract, answer: AnswerContract) -> OutputContract:
        """Write the answer that the user gave."""
        return output.write_message(answer).write_message(NewLine())
