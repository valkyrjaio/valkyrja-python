#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from typing import Any, Self, final, override

from valkyrja.type.contract.type_contract import TypeContract


@final
class StringTypeFixture(TypeContract):
    """A type that holds a string, standing in for the Type component."""

    def __init__(self, value: str) -> None:
        self.value = value

    @override
    def as_value(self) -> Any:
        return self.value

    @override
    def as_flat_value(self) -> str | int | float | bool | None:
        return self.value

    @override
    def modify(self, closure: Callable[[Any], Any]) -> Self:
        return type(self)(closure(self.value))
