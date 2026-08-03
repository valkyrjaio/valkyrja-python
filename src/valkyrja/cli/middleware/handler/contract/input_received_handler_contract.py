#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.handler_contract import HandlerContract


class InputReceivedHandlerContract(HandlerContract):
    """Runs each middleware for a received input."""

    @abstractmethod
    def input_received(self, input_: InputContract) -> InputContract | OutputContract:
        """Run the chain, and get the input onward or an output that stops it."""
