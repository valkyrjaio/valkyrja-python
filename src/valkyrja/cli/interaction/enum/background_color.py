#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import IntEnum

DEFAULT_BACKGROUND_COLOR = 49
"""The ANSI code that returns the background to the color of the terminal."""


class BackgroundColor(IntEnum):
    """The ANSI code that sets the color behind the text."""

    BLACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47
    DARK_GRAY = 100
    LIGHT_RED = 101
    LIGHT_GREEN = 102
    LIGHT_YELLOW = 103
    LIGHT_BLUE = 104
    LIGHT_MAGENTA = 105
    LIGHT_CYAN = 106
    LIGHT_WHITE = 107

    def get_default(self) -> int:
        """Get the code that returns the background to the color of the terminal."""
        return DEFAULT_BACKGROUND_COLOR
