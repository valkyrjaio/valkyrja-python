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
from valkyrja.cli.interaction.message.contract.answer_contract import (
    AnswerContract,
    ResponseValidator,
)
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_validation_callable_exception import (
    CliInteractionNoValidationCallableException,
)

DEFAULT_ANSWER_TEXT = "You answered: `%s`"


class Answer(Message, AnswerContract):
    """The answer that a user gives to a question."""

    def __init__(
        self,
        default_response: str,
        validation_callable: ResponseValidator | None = None,
        has_been_answered: bool = False,
        text: str = DEFAULT_ANSWER_TEXT,
        formatter: FormatterContract | None = None,
        allowed_responses: list[str] | None = None,
    ) -> None:
        super().__init__(text, formatter)

        responses = list(allowed_responses) if allowed_responses is not None else []

        if default_response not in responses:
            responses.append(default_response)

        self._default_response = default_response
        self._validation_callable = validation_callable
        self._has_been_answered = has_been_answered
        self._user_response = default_response
        self._allowed_responses = responses

    @override
    def get_text(self) -> str:
        return self._text % self._user_response

    @override
    def get_default_response(self) -> str:
        return self._default_response

    @override
    def with_default_response(self, default_response: str) -> Self:
        new = copy(self)
        new._allowed_responses = list(self._allowed_responses)

        if not new._has_been_answered:
            new._user_response = default_response

        new._default_response = default_response

        if default_response not in new._allowed_responses:
            new._allowed_responses.append(default_response)

        return new

    @override
    def get_allowed_responses(self) -> list[str]:
        return list(self._allowed_responses)

    @override
    def with_allowed_responses(self, *allowed_responses: str) -> Self:
        new = copy(self)
        new._allowed_responses = list(allowed_responses)

        if new._default_response not in new._allowed_responses:
            new._allowed_responses.append(new._default_response)

        return new

    @override
    def get_user_response(self) -> str:
        return self._user_response

    @override
    def with_user_response(self, user_response: str) -> Self:
        new = copy(self)
        new._user_response = user_response

        return new

    @override
    def has_validation_callable(self) -> bool:
        return self._validation_callable is not None

    @override
    def get_validation_callable(self) -> ResponseValidator:
        if self._validation_callable is None:
            raise CliInteractionNoValidationCallableException("No validation callable has been set")

        return self._validation_callable

    @override
    def with_validation_callable(self, validation_callable: ResponseValidator) -> Self:
        new = copy(self)
        new._validation_callable = validation_callable

        return new

    @override
    def without_validation_callable(self) -> Self:
        new = copy(self)
        new._validation_callable = None

        return new

    @override
    def has_been_answered(self) -> bool:
        return self._has_been_answered

    @override
    def with_has_been_answered(self, has_been_answered: bool) -> Self:
        new = copy(self)
        new._has_been_answered = has_been_answered

        return new

    @override
    def is_valid_response(self) -> bool:
        return self._user_response in self._allowed_responses or (
            self._validation_callable is not None and self._validation_callable(self._user_response)
        )
