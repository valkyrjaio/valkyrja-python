#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.enum.text_color import TextColor
from valkyrja.cli.interaction.format.format import Format


class TextColorFormat(Format):
    """The format that sets the color of the text."""

    def __init__(self, value: TextColor) -> None:
        super().__init__(str(value.value), str(value.get_default()))
