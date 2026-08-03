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
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)


class ThrowableCaughtMiddlewareContract(ABC):
    """Runs after the application catches a throwable during the dispatch."""

    @abstractmethod
    def throwable_caught(
        self,
        input_: InputContract,
        output: OutputContract,
        throwable: BaseException,
        handler: ThrowableCaughtHandlerContract,
    ) -> OutputContract:
        """Get the output that the application writes for the throwable."""
