#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.header.value.component.contract.component_contract import (
    ComponentContract,
)

COMPONENT_SEPARATOR = "="
"""What stands between the token and the text of a component."""


class Component(ComponentContract):
    """One part of a header value, such as `charset=utf-8`."""

    def __init__(self, token: str, text: str = "") -> None:
        self._token = token
        self._text = text

    @override
    def __str__(self) -> str:
        if self._text == "":
            return self._token

        return f"{self._token}{COMPONENT_SEPARATOR}{self._text}"

    @override
    def get_token(self) -> str:
        return self._token

    @override
    def with_token(self, token: str) -> Self:
        new = copy(self)
        new._token = token

        return new

    @override
    def get_text(self) -> str:
        return self._text

    @override
    def with_text(self, text: str) -> Self:
        new = copy(self)
        new._text = text

        return new

    @staticmethod
    def from_string(component: str) -> Component:
        """Build a component from the string that a header carries."""
        token, separator, text = component.partition(COMPONENT_SEPARATOR)

        return Component(token.strip(), text.strip() if separator else "")
