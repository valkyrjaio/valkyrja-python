#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import IntEnum

DEFAULT_STYLE = 28
"""The ANSI code that ends every style the other codes do not name."""


class Style(IntEnum):
    """The ANSI code that sets the style of the text."""

    BOLD = 1
    UNDERSCORE = 4
    BLINK = 5
    INVERSE = 7
    CONCEAL = 8

    def get_default(self) -> int:
        """Get the code that ends this style."""
        match self:
            case Style.BOLD:
                return 22
            case Style.UNDERSCORE:
                return 24
            case Style.BLINK:
                return 25
            case Style.INVERSE:
                return 27
            case _:
                return DEFAULT_STYLE
