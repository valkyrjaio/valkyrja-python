#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import io
import sys
from typing import TextIO, cast, final

from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream


class ReadOnlyStringIO(io.StringIO):
    """A stream in memory that reports itself read-only.

    `Mode.READ` names a stream that a caller reads and never writes. A plain
    `StringIO` reports itself writable whatever the mode says.
    """

    def writable(self) -> bool:
        return False


@final
class StreamFactory:
    """Opens the stream that a caller names."""

    @staticmethod
    def get_resource_stream(
        stream: StandardStream | str = StandardStream.MEMORY, mode: Mode = Mode.WRITE_READ
    ) -> TextIO:
        """Get the stream that the name points at.

        A `StandardStream` names a stream that the process holds open. Any other
        string is a path, and the factory opens it.
        """
        if isinstance(stream, StandardStream):
            return StreamFactory._get_standard_stream(stream, mode)

        return cast("TextIO", open(stream, mode.value, encoding="utf-8"))

    @staticmethod
    def _get_standard_stream(stream: StandardStream, mode: Mode) -> TextIO:
        """Get the stream that the process holds open under a given name."""
        match stream:
            case StandardStream.STDIN:
                return sys.stdin
            case StandardStream.STDOUT:
                return sys.stdout
            case StandardStream.STDERR:
                return sys.stderr
            case _:
                return ReadOnlyStringIO() if mode is Mode.READ else io.StringIO()
