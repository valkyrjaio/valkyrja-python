#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.enum.background_color import BackgroundColor
from valkyrja.cli.interaction.format.format import Format


class BackgroundColorFormat(Format):
    """The format that sets the color behind the text."""

    def __init__(self, value: BackgroundColor) -> None:
        super().__init__(str(value.value), str(value.get_default()))
