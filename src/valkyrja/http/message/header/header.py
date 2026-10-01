#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Iterator
from copy import copy
from typing import Self, override

from valkyrja.http.message.header.contract.header_contract import HeaderContract
from valkyrja.http.message.header.factory.header_factory import HeaderFactory
from valkyrja.http.message.header.throwable.exception.http_header_unsupported_offset_set_exception import (
    HttpHeaderUnsupportedOffsetSetException,
)
from valkyrja.http.message.header.throwable.exception.http_header_unsupported_offset_unset_exception import (
    HttpHeaderUnsupportedOffsetUnsetException,
)
from valkyrja.http.message.header.value.contract.value_contract import ValueContract
from valkyrja.http.message.header.value.value import Value

HEADER_SEPARATOR = ": "
"""What stands between the name of a header and its values."""

VALUES_SEPARATOR = ", "
"""What stands between one value of a header and the next."""


class Header(HeaderContract):
    def __init__(self, name: str, *values: ValueContract | str) -> None:
        HeaderFactory.assert_valid_name(name)

        self._name = name
        self._normalized_name = name.lower()
        self._values: list[ValueContract] = self._to_values(values)

    @classmethod
    def from_value(cls, value: str) -> Header:
        """Build a header from one line, which names the header before the colon."""
        name = value
        values_as_string = ""

        if ":" in value:
            name, values_as_string = value.split(":", 1)

        values = values_as_string.split(",") if "," in values_as_string else [values_as_string]

        return cls(name, *values) if values_as_string != "" else cls(name)

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
        HeaderFactory.assert_valid_name(name)

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

    @override
    def __getitem__(self, index: int) -> ValueContract:
        return self._values[index]

    @override
    def __setitem__(self, index: int, value: ValueContract | str) -> None:
        raise HttpHeaderUnsupportedOffsetSetException("Use with_values or with_added_values")

    @override
    def __delitem__(self, index: int) -> None:
        raise HttpHeaderUnsupportedOffsetUnsetException("Use with_values or with_added_values")

    @override
    def __len__(self) -> int:
        return len(self._values)

    @override
    def __iter__(self) -> Iterator[ValueContract]:
        return iter(self._values)

    @staticmethod
    def _to_values(values: tuple[ValueContract | str, ...]) -> list[ValueContract]:
        """Take a value as it is, and build one from a string.

        Each value passes the check that RFC 7230 states, so no value splits the
        response that carries the header.
        """
        built: list[ValueContract] = []

        for value in values:
            built.append(value if isinstance(value, ValueContract) else Value.from_string(value))
            HeaderFactory.assert_valid_value(str(built[-1]))

        return built
