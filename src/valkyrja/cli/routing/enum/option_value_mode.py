#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum, auto


class OptionValueMode(Enum):
    """Says whether the option takes no value, one value, or many."""

    NONE = auto()
    DEFAULT = auto()
    ARRAY = auto()
