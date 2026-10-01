#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import io
import sys
from pathlib import Path
from typing import BinaryIO, cast, final

from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_stream_exception import (
    HttpStreamInvalidStreamException,
)

NO_TRUNCATE_MODES = (Mode.WRITE_CREATE, Mode.WRITE_READ_CREATE)
"""PHP's `c` and `c+` open a file without truncating it, and create it when absent."""


class ReadOnlyBytesIO(io.BytesIO):
    def writable(self) -> bool:
        return False


@final
class StreamFactory:
    @staticmethod
    def get_resource_stream(
        stream: StandardStream | str = StandardStream.MEMORY, mode: Mode = Mode.WRITE_READ
    ) -> BinaryIO:
        """Get the stream that the name points at.

        A `StandardStream` names a stream that the process holds open. Any other
        string is a path, and the factory opens it in binary, because a body is bytes.
        """
        if isinstance(stream, StandardStream):
            return StreamFactory._get_standard_stream(stream, mode)

        return StreamFactory._get_file_stream(stream, mode)

    @staticmethod
    def is_standard_stream(stream: object) -> bool:
        """Get whether the process owns the stream, rather than this component.

        A component that closes one of these takes it from every other reader of
        the process, so the component leaves it open.
        """
        return stream in (
            sys.stdin,
            sys.stdout,
            sys.stderr,
            getattr(sys.stdin, "buffer", None),
            getattr(sys.stdout, "buffer", None),
            getattr(sys.stderr, "buffer", None),
        )

    @staticmethod
    def _get_file_stream(path: str, mode: Mode) -> BinaryIO:
        """Open a file in binary, under the mode that the caller names."""
        try:
            if mode in NO_TRUNCATE_MODES:
                return StreamFactory._get_no_truncate_file_stream(path)

            return cast("BinaryIO", Path(path).open(f"{mode.value}b"))
        except OSError as exception:
            raise HttpStreamInvalidStreamException(f"Unable to open the stream `{path}`") from exception

    @staticmethod
    def _get_no_truncate_file_stream(path: str) -> BinaryIO:
        """Open a file for reading and writing, and create it when it is absent.

        Python has no mode for this. `r+b` keeps the contents and refuses a file that
        is absent, and `w+b` creates one and truncates it, so the choice turns on
        whether the file is there.
        """
        file = Path(path)
        mode = "r+b" if file.exists() else "w+b"

        return cast("BinaryIO", file.open(mode))

    @staticmethod
    def _get_standard_stream(stream: StandardStream, mode: Mode) -> BinaryIO:
        """Get the stream that the process holds open under a given name."""
        match stream:
            case StandardStream.STDIN:
                return StreamFactory._get_buffer(sys.stdin)
            case StandardStream.STDOUT:
                return StreamFactory._get_buffer(sys.stdout)
            case StandardStream.STDERR:
                return StreamFactory._get_buffer(sys.stderr)
            case _:
                return ReadOnlyBytesIO() if mode is Mode.READ else io.BytesIO()

    @staticmethod
    def _get_buffer(stream: object) -> BinaryIO:
        """Get the byte buffer of a text stream of the process.

        A test replaces one of these with a text object that holds no buffer, and
        that object answers the write itself.
        """
        return cast("BinaryIO", getattr(stream, "buffer", stream))
