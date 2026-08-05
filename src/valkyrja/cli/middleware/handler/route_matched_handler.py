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
from valkyrja.cli.middleware.contract.route_matched_middleware_contract import (
    RouteMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteMatchedHandler(Handler, RouteMatchedHandlerContract):
    """Runs each middleware for a route that a command matched."""

    @override
    def route_matched(self, input_: InputContract, route: RouteContract) -> RouteContract | OutputContract:
        next_middleware = self._next

        if next_middleware is None:
            return route

        middleware = cast("RouteMatchedMiddlewareContract", self._get_middleware(next_middleware))

        return middleware.route_matched(input_, route, self)
