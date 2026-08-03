#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import TYPE_CHECKING, cast, override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.route_dispatched_middleware_contract import (
    RouteDispatchedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.route_dispatched_handler_contract import (
    RouteDispatchedHandlerContract,
)

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteDispatchedHandler(Handler, RouteDispatchedHandlerContract):
    """Runs each middleware for a route that the application dispatched."""

    @override
    def route_dispatched(self, input_: InputContract, output: OutputContract, route: RouteContract) -> OutputContract:
        next_middleware = self._next

        if next_middleware is None:
            return output

        middleware = cast("RouteDispatchedMiddlewareContract", self._get_middleware(next_middleware))

        return middleware.route_dispatched(input_, output, route, self)
