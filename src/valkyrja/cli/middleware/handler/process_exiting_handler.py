#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import cast, override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.process_exiting_middleware_contract import (
    ProcessExitingMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)


class ProcessExitingHandler(Handler, ProcessExitingHandlerContract):
    """Runs each middleware as the process exits."""

    @override
    def process_exiting(self, input_: InputContract, output: OutputContract) -> None:
        next_middleware = self._next

        if next_middleware is not None:
            cast("ProcessExitingMiddlewareContract", self._get_middleware(next_middleware)).process_exiting(
                input_, output, self
            )
