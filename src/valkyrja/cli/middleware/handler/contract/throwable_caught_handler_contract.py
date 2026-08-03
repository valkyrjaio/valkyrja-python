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


class ThrowableCaughtHandlerContract(HandlerContract):
    """Runs each middleware for a throwable that the application caught."""

    @abstractmethod
    def throwable_caught(
        self, input_: InputContract, output: OutputContract, throwable: BaseException
    ) -> OutputContract:
        """Run the chain, and get the output that the application writes."""
