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
from valkyrja.cli.middleware.contract.route_matched_middleware_contract import (
    RouteMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)
from valkyrja.cli.routing.data.contract.route_contract import RouteContract

SHORT_CIRCUIT_MIDDLEWARE_ID = "Valkyrja.Tests.Middleware.ShortCircuit"


@final
class ShortCircuitMiddlewareFixture(RouteMatchedMiddlewareContract):
    """A middleware that answers with an output and stops the chain."""

    @override
    def route_matched(
        self, input_: InputContract, route: RouteContract, handler: RouteMatchedHandlerContract
    ) -> RouteContract | OutputContract:
        return EmptyOutput(exit_code=ExitCode.USAGE_ERROR)
