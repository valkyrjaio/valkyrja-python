#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.message.messages import Messages
from valkyrja.cli.interaction.message.new_line import NewLine


class Banner(Message):
    """A message that puts a block of color around a text."""

    def __init__(self, message: Message) -> None:
        super().__init__(message.get_text())

        text = f"    {message.get_text()}    "
        spaces = " " * len(text)

        self._messages = Messages(
            NewLine(),
            message.with_text(spaces),
            NewLine(),
            message.with_text(text),
            NewLine(),
            message.with_text(spaces),
            NewLine(),
        )

    @override
    def get_text(self) -> str:
        return self._messages.get_text()

    @override
    def get_formatted_text(self) -> str:
        return self._messages.get_formatted_text()
