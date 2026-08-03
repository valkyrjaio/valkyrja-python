#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.cli.interaction.message.answer import Answer
from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.contract.question_contract import QuestionCallback
from valkyrja.cli.interaction.message.question import Question
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract


def pass_through(output: OutputContract, answer: AnswerContract) -> OutputContract:
    """Answer with the output that the writer gave."""
    return output


@final
class RecordingQuestionFixture(Question):
    """A question that reads a scripted response instead of the terminal."""

    def __init__(
        self,
        text: str,
        answer: Answer,
        responses: list[str] | None = None,
        callback: QuestionCallback = pass_through,
    ) -> None:
        super().__init__(text, callback, answer)

        # A `with_` method copies the question, and a shallow copy shares a list.
        # The counter is therefore a list, so a copy records onto the same one.
        self.responses = list(responses) if responses is not None else []
        self.read_log: list[str] = []

    @property
    def reads(self) -> int:
        """Get how many times the question read a response."""
        return len(self.read_log)

    @override
    def _read_response(self) -> str:
        response = self.responses.pop(0) if self.responses else ""

        self.read_log.append(response)

        return response
