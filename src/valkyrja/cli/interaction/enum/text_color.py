#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import IntEnum

DEFAULT_TEXT_COLOR = 39
"""The ANSI code that returns the text to the color of the terminal."""


class TextColor(IntEnum):
    """The ANSI code that sets the color of the text."""

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37
    DARK_GRAY = 90
    LIGHT_RED = 91
    LIGHT_GREEN = 92
    LIGHT_YELLOW = 93
    LIGHT_BLUE = 94
    LIGHT_MAGENTA = 95
    LIGHT_CYAN = 96
    LIGHT_WHITE = 97

    def get_default(self) -> int:
        """Get the code that returns the text to the color of the terminal."""
        return DEFAULT_TEXT_COLOR
