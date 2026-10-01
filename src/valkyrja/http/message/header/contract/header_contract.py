#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Self

from valkyrja.http.message.header.value.contract.value_contract import ValueContract


class HeaderContract(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """Get the header as one line, with the name in front of it."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the header, as the caller wrote it."""

    @abstractmethod
    def get_normalized_name(self) -> str:
        """Get the name of the header in lower case."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the header that carries a different name."""

    @abstractmethod
    def get_values(self) -> list[ValueContract]:
        """Get each value of the header."""

    @abstractmethod
    def with_values(self, *values: ValueContract | str) -> Self:
        """Get a copy of the header that carries different values."""

    @abstractmethod
    def with_added_values(self, *values: ValueContract | str) -> Self:
        """Get a copy of the header that carries more values."""

    @abstractmethod
    def get_header_line(self) -> str:
        """Get every value of the header, joined by a comma."""

    @abstractmethod
    def __getitem__(self, index: int) -> ValueContract:
        """Get the value that sits at one position."""

    @abstractmethod
    def __setitem__(self, index: int, value: ValueContract | str) -> None:
        """Refuse the write, because a header is immutable."""

    @abstractmethod
    def __delitem__(self, index: int) -> None:
        """Refuse the removal, because a header is immutable."""

    @abstractmethod
    def __len__(self) -> int:
        """Get how many values the header carries."""

    @abstractmethod
    def __iter__(self) -> Iterator[ValueContract]:
        """Read each value of the header in turn."""
