#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from collections.abc import Callable
from typing import Self

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract

type ResponseValidator = Callable[[str], bool]
"""The answer calls this validator to decide whether a response is valid."""


class AnswerContract(MessageContract):
    """The contract for the answer that a user gives to a question."""

    @abstractmethod
    def get_default_response(self) -> str:
        """Get the response that the answer takes when the user gives none."""

    @abstractmethod
    def with_default_response(self, default_response: str) -> Self:
        """Get a copy of the answer that carries a different default response."""

    @abstractmethod
    def get_allowed_responses(self) -> list[str]:
        """Get each response that the answer accepts."""

    @abstractmethod
    def with_allowed_responses(self, *allowed_responses: str) -> Self:
        """Get a copy of the answer that accepts different responses."""

    @abstractmethod
    def get_user_response(self) -> str:
        """Get the response that the user gave."""

    @abstractmethod
    def with_user_response(self, user_response: str) -> Self:
        """Get a copy of the answer that carries a different user response."""

    @abstractmethod
    def has_validation_callable(self) -> bool:
        """Get whether the answer carries a validator."""

    @abstractmethod
    def get_validation_callable(self) -> ResponseValidator:
        """Get the validator of the answer."""

    @abstractmethod
    def with_validation_callable(self, validation_callable: ResponseValidator) -> Self:
        """Get a copy of the answer that carries a different validator."""

    @abstractmethod
    def without_validation_callable(self) -> Self:
        """Get a copy of the answer that carries no validator."""

    @abstractmethod
    def has_been_answered(self) -> bool:
        """Get whether the user answered already."""

    @abstractmethod
    def with_has_been_answered(self, has_been_answered: bool) -> Self:
        """Get a copy of the answer that records whether the user answered."""

    @abstractmethod
    def is_valid_response(self) -> bool:
        """Get whether the response of the user is valid."""
