#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any, TextIO

SEEK_SET = 0
"""Seek from the start of the stream."""


class StreamContract(ABC):
    """The contract for the body of a message."""

    @abstractmethod
    def __str__(self) -> str:
        """Get every byte of the stream as a string."""

    @abstractmethod
    def close(self) -> None:
        """Close the stream."""

    @abstractmethod
    def detach(self) -> TextIO | None:
        """Take the stream away, and leave this object with none."""

    @abstractmethod
    def get_size(self) -> int:
        """Get how many bytes the stream holds."""

    @abstractmethod
    def tell(self) -> int:
        """Get where the stream reads next."""

    @abstractmethod
    def eof(self) -> bool:
        """Get whether the stream reached the end."""

    @abstractmethod
    def is_seekable(self) -> bool:
        """Get whether the stream moves to a different place."""

    @abstractmethod
    def seek(self, offset: int, whence: int = SEEK_SET) -> None:
        """Move to a different place in the stream."""

    @abstractmethod
    def rewind(self) -> None:
        """Move to the start of the stream."""

    @abstractmethod
    def is_writable(self) -> bool:
        """Get whether the stream takes a write."""

    @abstractmethod
    def write(self, string: str) -> int:
        """Write to the stream, and get how many bytes it took."""

    @abstractmethod
    def is_readable(self) -> bool:
        """Get whether the stream gives a read."""

    @abstractmethod
    def read(self, length: int) -> str:
        """Read a number of bytes from the stream."""

    @abstractmethod
    def get_contents(self) -> str:
        """Read the rest of the stream."""

    @abstractmethod
    def get_metadata(self) -> dict[str, Any]:
        """Get everything that the stream says about itself."""

    @abstractmethod
    def get_metadata_item(self, key: str) -> Any:
        """Get one thing that the stream says about itself."""
