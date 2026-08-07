#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)


class InputReceivedMiddlewareContract(ABC):
    @abstractmethod
    def input_received(
        self, input_: InputContract, handler: InputReceivedHandlerContract
    ) -> InputContract | OutputContract:
        """Take the input onward, or answer with an output and stop the chain."""
