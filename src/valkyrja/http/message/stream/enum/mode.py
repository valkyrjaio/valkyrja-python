#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class Mode(Enum):
    """The mode that a stream opens in.

    PHP also carries a `ModeTranslation` enum for the `b` and `t` suffixes.
    Python has no such suffix on a text stream, so this port carries the mode
    alone.
    """

    READ = "r"
    READ_WRITE = "r+"
    WRITE = "w"
    WRITE_READ = "w+"
    WRITE_END = "a"
    WRITE_READ_END = "a+"
    CREATE_WRITE = "x"
    CREATE_WRITE_READ = "x+"
    WRITE_CREATE = "c"
    WRITE_READ_CREATE = "c+"
