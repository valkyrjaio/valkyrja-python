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


class ProcessExitingHandlerContract(HandlerContract):
    """Runs each middleware as the process exits."""

    @abstractmethod
    def process_exiting(self, input_: InputContract, output: OutputContract) -> None:
        """Run the chain."""
