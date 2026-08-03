#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum, auto


class ArgumentValueMode(Enum):
    """Says whether the argument takes one value or many."""

    DEFAULT = auto()
    ARRAY = auto()
