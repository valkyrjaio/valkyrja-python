#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.empty_output_contract import EmptyOutputContract
from valkyrja.cli.interaction.output.output import Output


class EmptyOutput(Output, EmptyOutputContract):
    """An output that writes nothing, and still records each message."""

    @override
    def _output_message(self, message: MessageContract) -> None:
        """Write nothing. The output records the message and stops there."""
