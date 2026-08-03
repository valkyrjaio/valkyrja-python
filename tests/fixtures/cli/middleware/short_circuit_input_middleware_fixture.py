#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)

SHORT_CIRCUIT_INPUT_MIDDLEWARE_ID = "Valkyrja.Tests.Middleware.ShortCircuitInput"


@final
class ShortCircuitInputMiddlewareFixture(InputReceivedMiddlewareContract):
    """A middleware that answers with an output before the router runs."""

    @override
    def input_received(
        self, input_: InputContract, handler: InputReceivedHandlerContract
    ) -> InputContract | OutputContract:
        return EmptyOutput(exit_code=ExitCode.NO_INPUT)
