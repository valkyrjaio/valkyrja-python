#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract
from valkyrja.cli.interaction.formatter.question_formatter import QuestionFormatter
from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.contract.question_contract import (
    QuestionCallback,
    QuestionContract,
)
from valkyrja.cli.interaction.message.message import Message


class Unset:
    """The absence of an argument, which is not the same as `None`."""


UNSET = Unset()
"""Stands for the formatter that the caller did not name."""


class Question(Message, QuestionContract):
    def __init__(
        self,
        text: str,
        callback: QuestionCallback,
        answer: AnswerContract,
        formatter: FormatterContract | Unset | None = UNSET,
    ) -> None:
        # The sentinel keeps `None` meaning no formatter, which PHP gets from a
        # default that names the formatter rather than null.
        super().__init__(text, QuestionFormatter() if isinstance(formatter, Unset) else formatter)

        self._callback = callback
        self._answer = answer

    @override
    def get_callable(self) -> QuestionCallback:
        return self._callback

    @override
    def with_callable(self, callback: QuestionCallback) -> Self:
        new = copy(self)
        new._callback = callback

        return new

    @override
    def get_answer(self) -> AnswerContract:
        return self._answer

    @override
    def with_answer(self, answer: AnswerContract) -> Self:
        new = copy(self)
        new._answer = answer

        return new

    @override
    def ask(self) -> AnswerContract:
        response = self._read_response()

        # An empty response is no answer, so the default of the answer stands.
        if response == "":
            return self._answer

        return self._answer.with_user_response(response)

    def _read_response(self) -> str:
        """Read one line from the user.

        The method is a seam. A test overrides it, because a test cannot type
        into the terminal that the process reads.
        """
        try:
            return input().strip()
        except EOFError:
            # A closed input reads no line, which PHP reports as a false `fgets`.
            # An empty response leaves the answer as it is.
            return ""
