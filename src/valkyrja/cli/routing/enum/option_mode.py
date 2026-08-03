#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum, auto


class OptionMode(Enum):
    """Says whether a command needs the option."""

    REQUIRED = auto()
    OPTIONAL = auto()
