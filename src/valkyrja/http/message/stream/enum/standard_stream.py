#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class StandardStream(Enum):
    """A stream that the process holds open already.

    PHP names each one with a `php://` wrapper, and it opens the wrapper by
    path. Python holds each one as an object on `sys`, so the factory reads this
    enum and answers with that object.
    """

    STDIN = "stdin"
    STDOUT = "stdout"
    STDERR = "stderr"
    MEMORY = "memory"
    """A stream in memory. It answers `php://temp` and `php://memory`."""
