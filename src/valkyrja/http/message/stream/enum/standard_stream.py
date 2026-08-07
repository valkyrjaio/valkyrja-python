#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class StandardStream(Enum):
    STDIN = "stdin"
    STDOUT = "stdout"
    STDERR = "stderr"
    MEMORY = "memory"
    """A stream in memory. It answers `php://temp` and `php://memory`."""
