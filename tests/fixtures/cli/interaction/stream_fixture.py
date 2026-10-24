#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from io import StringIO
from typing import final, override


@final
class RaisingStreamFixture(StringIO):
    """A stream whose write reports a failure of the device."""

    @override
    def write(self, s: str, /) -> int:
        raise OSError("the device reported a failure")


@final
class RefusingStreamFixture(StringIO):
    """A stream that takes no character of what it is offered."""

    @override
    def write(self, s: str, /) -> int:
        return 0


@final
class PartialStreamFixture(StringIO):
    """A stream that takes one character of each offer, as a non-blocking stream does."""

    @override
    def write(self, s: str, /) -> int:
        super().write(s[0])

        return 1
