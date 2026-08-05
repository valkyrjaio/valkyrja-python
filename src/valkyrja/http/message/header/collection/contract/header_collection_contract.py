#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.http.message.header.contract.header_contract import HeaderContract


class HeaderCollectionContract(ABC):
    """The contract for the headers that a message carries."""

    @abstractmethod
    def has(self, name: str) -> bool:
        """Get whether the collection holds a header with a given name."""

    @abstractmethod
    def get(self, name: str) -> HeaderContract:
        """Get the header that carries a given name."""

    @abstractmethod
    def get_header_line(self, name: str) -> str:
        """Get every value of one header, joined by a comma."""

    @abstractmethod
    def get_all(self) -> list[HeaderContract]:
        """Get every header."""

    @abstractmethod
    def get_only(self, *names: str) -> list[HeaderContract]:
        """Get the header for each name that the caller gives."""

    @abstractmethod
    def get_all_except(self, *names: str) -> list[HeaderContract]:
        """Get every header except the ones that the caller names."""

    @abstractmethod
    def with_header(self, header: HeaderContract) -> Self:
        """Get a copy of the collection that holds one more header."""

    @abstractmethod
    def without_header(self, name: str) -> Self:
        """Get a copy of the collection without the header of a given name."""
