#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Self

from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract

if TYPE_CHECKING:
    from valkyrja.cli.interaction.output.contract.output_contract import OutputContract

type QuestionCallback = Callable[["OutputContract", AnswerContract], "OutputContract"]
"""The question calls this callback once the user answers."""


class QuestionContract(MessageContract):
    """The contract for a message that asks the user a question.

    The import of `OutputContract` is for the type checker alone. An output
    writes a question, so a plain import would make the two modules import each
    other.
    """

    @abstractmethod
    def get_callable(self) -> QuestionCallback:
        """Get the callback that runs once the user answers."""

    @abstractmethod
    def with_callable(self, callback: QuestionCallback) -> Self:
        """Get a copy of the question that carries a different callback."""

    @abstractmethod
    def get_answer(self) -> AnswerContract:
        """Get the answer of the question."""

    @abstractmethod
    def with_answer(self, answer: AnswerContract) -> Self:
        """Get a copy of the question that carries a different answer."""

    @abstractmethod
    def ask(self) -> AnswerContract:
        """Ask the user, and get the answer that holds the response."""
