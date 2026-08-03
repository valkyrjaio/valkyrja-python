#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.header.contract.header_contract import HeaderContract
from valkyrja.http.message.header.value.contract.value_contract import ValueContract
from valkyrja.http.message.header.value.value import Value

HEADER_SEPARATOR = ": "
"""What stands between the name of a header and its values."""

VALUES_SEPARATOR = ", "
"""What stands between one value of a header and the next."""


class Header(HeaderContract):
    """One header of a message."""

    def __init__(self, name: str, *values: ValueContract | str) -> None:
        self._name = name
        self._normalized_name = name.lower()
        self._values: list[ValueContract] = self._to_values(values)

    @override
    def __str__(self) -> str:
        line = self.get_header_line()

        if line == "":
            return ""

        return f"{self._name}{HEADER_SEPARATOR}{line}"

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def get_normalized_name(self) -> str:
        return self._normalized_name

    @override
    def with_name(self, name: str) -> Self:
        new = copy(self)
        new._name = name
        new._normalized_name = name.lower()

        return new

    @override
    def get_values(self) -> list[ValueContract]:
        return list(self._values)

    @override
    def with_values(self, *values: ValueContract | str) -> Self:
        new = copy(self)
        new._values = self._to_values(values)

        return new

    @override
    def with_added_values(self, *values: ValueContract | str) -> Self:
        new = copy(self)
        new._values = [*self._values, *self._to_values(values)]

        return new

    @override
    def get_header_line(self) -> str:
        return VALUES_SEPARATOR.join(str(value) for value in self._values)

    @staticmethod
    def _to_values(values: tuple[ValueContract | str, ...]) -> list[ValueContract]:
        """Take a value as it is, and build one from a string."""
        return [value if isinstance(value, ValueContract) else Value.from_string(value) for value in values]
