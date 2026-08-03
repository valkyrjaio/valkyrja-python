#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, TextIO, override

from valkyrja.http.message.stream.contract.stream_contract import SEEK_SET, StreamContract
from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream
from valkyrja.http.message.stream.factory.stream_factory import StreamFactory
from valkyrja.http.message.stream.throwable.exception.http_stream_exception import (
    HttpStreamException,
)


class Stream(StreamContract):
    """The body of a message, over a text stream.

    PHP opens a `php://` wrapper by path. Python holds each standard stream as
    an object on `sys`, and it holds a stream in memory as a `StringIO`, so the
    factory answers with the object rather than a path.
    """

    def __init__(
        self,
        stream: StandardStream | str = StandardStream.MEMORY,
        mode: Mode = Mode.WRITE_READ,
    ) -> None:
        self._stream: TextIO | None = StreamFactory.get_resource_stream(stream, mode)

    @override
    def __str__(self) -> str:
        if not self.is_readable():
            return ""

        self.rewind()

        return self.get_contents()

    @override
    def close(self) -> None:
        if self._stream is not None:
            self._stream.close()

            self._stream = None

    @override
    def detach(self) -> TextIO | None:
        stream = self._stream

        self._stream = None

        return stream

    @override
    def get_size(self) -> int:
        stream = self._get_stream()
        place = stream.tell()

        stream.seek(0, 2)

        size = stream.tell()

        stream.seek(place)

        return size

    @override
    def tell(self) -> int:
        return self._get_stream().tell()

    @override
    def eof(self) -> bool:
        if self._stream is None:
            return True

        return self._stream.tell() >= self.get_size()

    @override
    def is_seekable(self) -> bool:
        return self._stream is not None and self._stream.seekable()

    @override
    def seek(self, offset: int, whence: int = SEEK_SET) -> None:
        if not self.is_seekable():
            raise HttpStreamException("The stream is not seekable")

        self._get_stream().seek(offset, whence)

    @override
    def rewind(self) -> None:
        self.seek(0)

    @override
    def is_writable(self) -> bool:
        return self._stream is not None and self._stream.writable()

    @override
    def write(self, string: str) -> int:
        if not self.is_writable():
            raise HttpStreamException("The stream is not writable")

        return self._get_stream().write(string)

    @override
    def is_readable(self) -> bool:
        return self._stream is not None and self._stream.readable()

    @override
    def read(self, length: int) -> str:
        if not self.is_readable():
            raise HttpStreamException("The stream is not readable")

        return self._get_stream().read(length)

    @override
    def get_contents(self) -> str:
        if not self.is_readable():
            raise HttpStreamException("The stream is not readable")

        return self._get_stream().read()

    @override
    def get_metadata(self) -> dict[str, Any]:
        stream = self._stream

        if stream is None:
            return {}

        return {
            "mode": getattr(stream, "mode", ""),
            "seekable": stream.seekable(),
            "readable": stream.readable(),
            "writable": stream.writable(),
        }

    @override
    def get_metadata_item(self, key: str) -> Any:
        return self.get_metadata().get(key)

    def _get_stream(self) -> TextIO:
        """Get the stream, and report a stream that a caller detached already."""
        if self._stream is None:
            raise HttpStreamException("The stream is detached")

        return self._stream
