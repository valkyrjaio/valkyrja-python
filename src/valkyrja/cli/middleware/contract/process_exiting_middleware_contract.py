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
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)


class ProcessExitingMiddlewareContract(ABC):
    """Runs as the process exits, after the application writes the output."""

    @abstractmethod
    def process_exiting(
        self, input_: InputContract, output: OutputContract, handler: ProcessExitingHandlerContract
    ) -> None:
        """Do the last work of the process."""
