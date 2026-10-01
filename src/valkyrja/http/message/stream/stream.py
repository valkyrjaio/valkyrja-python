#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, BinaryIO, override

from valkyrja.http.message.stream.contract.stream_contract import SEEK_SET, StreamContract
from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream
from valkyrja.http.message.stream.factory.stream_factory import StreamFactory
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_length_exception import (
    HttpStreamInvalidLengthException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_no_stream_available_exception import (
    HttpStreamNoStreamAvailableException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_read_exception import (
    HttpStreamStreamReadException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_seek_exception import (
    HttpStreamStreamSeekException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_tell_exception import (
    HttpStreamStreamTellException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_write_exception import (
    HttpStreamStreamWriteException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unreadable_stream_exception import (
    HttpStreamUnreadableStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unseekable_stream_exception import (
    HttpStreamUnseekableStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unwritable_stream_exception import (
    HttpStreamUnwritableStreamException,
)

ENCODING = "utf-8"
"""A body is bytes, and this encoding reads it as text."""


class Stream(StreamContract):
    def __init__(
        self,
        stream: StandardStream | str = StandardStream.MEMORY,
        mode: Mode = Mode.WRITE_READ,
    ) -> None:
        self._stream: BinaryIO | None = StreamFactory.get_resource_stream(stream, mode)

    @override
    def __str__(self) -> str:
        if not self.is_readable():
            return ""

        self.rewind()

        return self.get_contents().decode(ENCODING, errors="replace")

    @override
    def close(self) -> None:
        stream = self._stream

        if stream is None:
            return

        # A stream of the process belongs to the process, so closing it here would
        # take it from every other reader.
        if not StreamFactory.is_standard_stream(stream):
            stream.close()

        self._stream = None

    @override
    def detach(self) -> BinaryIO | None:
        stream = self._stream

        self._stream = None

        return stream

    @override
    def get_size(self) -> int:
        stream = self._get_stream()

        if not stream.seekable():
            return 0

        place = stream.tell()

        stream.seek(0, 2)

        size = stream.tell()

        stream.seek(place)

        return size

    @override
    def tell(self) -> int:
        stream = self._get_stream()

        try:
            return stream.tell()
        except OSError as exception:
            raise HttpStreamStreamTellException("Unable to read the position of the stream") from exception

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
            raise HttpStreamUnseekableStreamException("The stream is not seekable")

        try:
            self._get_stream().seek(offset, whence)
        except OSError as exception:
            raise HttpStreamStreamSeekException(f"Unable to seek to position {offset} of the stream") from exception

    @override
    def rewind(self) -> None:
        self.seek(0)

    @override
    def is_writable(self) -> bool:
        return self._stream is not None and self._stream.writable()

    @override
    def write(self, data: bytes | str) -> int:
        if not self.is_writable():
            raise HttpStreamUnwritableStreamException("The stream is not writable")

        payload = data.encode(ENCODING) if isinstance(data, str) else data

        try:
            return self._get_stream().write(payload)
        except OSError as exception:
            raise HttpStreamStreamWriteException("Unable to write to the stream") from exception

    @override
    def is_readable(self) -> bool:
        return self._stream is not None and self._stream.readable()

    @override
    def read(self, length: int) -> bytes:
        if not self.is_readable():
            raise HttpStreamUnreadableStreamException("The stream is not readable")

        if length < 0:
            raise HttpStreamInvalidLengthException(f"Invalid length `{length}` provided; must not be negative")

        try:
            return self._get_stream().read(length)
        except OSError as exception:
            raise HttpStreamStreamReadException("Unable to read from the stream") from exception

    @override
    def get_contents(self) -> bytes:
        if not self.is_readable():
            raise HttpStreamUnreadableStreamException("The stream is not readable")

        try:
            return self._get_stream().read()
        except OSError as exception:
            raise HttpStreamStreamReadException("Unable to read from the stream") from exception

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

    def _get_stream(self) -> BinaryIO:
        """Get the stream, and report a stream that a caller detached already."""
        if self._stream is None:
            raise HttpStreamNoStreamAvailableException("The stream is detached")

        return self._stream
