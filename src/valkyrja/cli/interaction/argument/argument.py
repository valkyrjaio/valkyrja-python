#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract


class Argument(ArgumentContract):
    """One positional argument that the user typed."""

    def __init__(self, value: str) -> None:
        self._value = value

    @override
    def get_value(self) -> str:
        return self._value

    @override
    def with_value(self, value: str) -> Self:
        new = copy(self)
        new._value = value

        return new
