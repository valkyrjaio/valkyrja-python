#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.enum.background_color import BackgroundColor
from valkyrja.cli.interaction.enum.text_color import TextColor
from valkyrja.cli.interaction.format.background_color_format import BackgroundColorFormat
from valkyrja.cli.interaction.format.text_color_format import TextColorFormat
from valkyrja.cli.interaction.formatter.formatter import Formatter


class ErrorFormatter(Formatter):
    """The formatter that marks an error."""

    def __init__(self) -> None:
        super().__init__(
            TextColorFormat(TextColor.LIGHT_WHITE),
            BackgroundColorFormat(BackgroundColor.RED),
        )
