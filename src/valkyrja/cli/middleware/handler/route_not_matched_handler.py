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
from valkyrja.cli.middleware.contract.route_not_matched_middleware_contract import (
    RouteNotMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.abstract.handler import Handler
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)


class RouteNotMatchedHandler(Handler, RouteNotMatchedHandlerContract):
    """Runs each middleware for a route that no command matched."""

    @override
    def route_not_matched(self, input_: InputContract, output: OutputContract) -> OutputContract:
        next_middleware = self._next

        if next_middleware is None:
            return output

        return cast("RouteNotMatchedMiddlewareContract", self._get_middleware(next_middleware)).route_not_matched(
            input_, output, self
        )
