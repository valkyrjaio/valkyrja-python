#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import io
from typing import final, override


@final
class FailingStreamFixture(io.BytesIO):
    """A stream whose every operation reports a failure of its device."""

    @override
    def tell(self) -> int:
        raise OSError("the device lost the position")

    @override
    def seek(self, offset: int, whence: int = io.SEEK_SET, /) -> int:
        raise OSError("the device refused the seek")

    @override
    def write(self, buffer: object, /) -> int:
        raise OSError("the device refused the write")

    @override
    def read(self, size: int | None = -1, /) -> bytes:
        raise OSError("the device refused the read")


@final
class UnseekableStreamFixture(io.BytesIO):
    """A stream that reads and writes, and that cannot seek."""

    @override
    def seekable(self) -> bool:
        return False
