#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.enum.option_type import OptionType
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract


class Option(OptionContract):
    """One named option that the user typed."""

    def __init__(self, name: str, value: str = "", type_: OptionType = OptionType.LONG) -> None:
        self._name = name
        self._value = value
        self._type = type_

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def with_name(self, name: str) -> Self:
        new = copy(self)
        new._name = name

        return new

    @override
    def has_value(self) -> bool:
        return self._value != ""

    @override
    def get_value(self) -> str:
        return self._value

    @override
    def with_value(self, value: str) -> Self:
        new = copy(self)
        new._value = value

        return new

    @override
    def without_value(self) -> Self:
        new = copy(self)
        new._value = ""

        return new

    @override
    def get_type(self) -> OptionType:
        return self._type

    @override
    def with_type(self, type_: OptionType) -> Self:
        new = copy(self)
        new._type = type_

        return new
