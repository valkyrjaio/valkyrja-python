#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.message import Message


class Messages(Message):
    """A message that joins several messages into one."""

    def __init__(self, *messages: MessageContract) -> None:
        super().__init__("")

        self._messages: list[MessageContract] = list(messages)

    @override
    def get_text(self) -> str:
        return "".join(message.get_text() for message in self._messages)

    @override
    def get_formatted_text(self) -> str:
        return "".join(message.get_formatted_text() for message in self._messages)
