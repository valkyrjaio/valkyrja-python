#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.interaction.formatter.contract.formatter_contract import FormatterContract
from valkyrja.cli.interaction.message.message import Message


class NewLine(Message):
    """A message that holds one line break."""

    def __init__(self, formatter: FormatterContract | None = None) -> None:
        super().__init__("\n", formatter)
