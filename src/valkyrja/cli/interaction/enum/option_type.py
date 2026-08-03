#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum, auto


class OptionType(Enum):
    """The form that an option takes on the command line."""

    SHORT = auto()
    """One dash and one letter, such as `-h`."""

    LONG = auto()
    """Two dashes and a word, such as `--help`."""
