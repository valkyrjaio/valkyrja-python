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
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.throwable.exception.cli_interaction_no_formatter_exception import (
    CliInteractionNoFormatterException,
)


class Message(MessageContract):
    """One message that an output writes."""

    def __init__(self, text: str, formatter: FormatterContract | None = None) -> None:
        self._text = text
        self._formatter = formatter

    @override
    def get_text(self) -> str:
        return self._text

    @override
    def get_formatted_text(self) -> str:
        if self._formatter is None:
            return self.get_text()

        return self._formatter.format_text(self.get_text())

    @override
    def with_text(self, text: str) -> Self:
        new = copy(self)
        new._text = text

        return new

    @override
    def has_formatter(self) -> bool:
        return self._formatter is not None

    @override
    def get_formatter(self) -> FormatterContract:
        if self._formatter is None:
            raise CliInteractionNoFormatterException("No formatter has been set")

        return self._formatter

    @override
    def with_formatter(self, formatter: FormatterContract) -> Self:
        new = copy(self)
        new._formatter = formatter

        return new

    @override
    def without_formatter(self) -> Self:
        new = copy(self)
        new._formatter = None

        return new
