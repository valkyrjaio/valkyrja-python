#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.enum.style import Style
from valkyrja.cli.interaction.format.format import Format


class StyleFormat(Format):
    """The format that sets the style of the text."""

    def __init__(self, value: Style) -> None:
        super().__init__(str(value.value), str(value.get_default()))
