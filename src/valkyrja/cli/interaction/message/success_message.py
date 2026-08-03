#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.formatter.success_formatter import SuccessFormatter
from valkyrja.cli.interaction.message.message import Message


class SuccessMessage(Message):
    """A message that reports a success."""

    def __init__(self, text: str) -> None:
        super().__init__(text=text, formatter=SuccessFormatter())
