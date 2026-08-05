#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteMatchedMiddlewareContract(ABC):
    """Runs after the application matches a route, and before it dispatches the route."""

    @abstractmethod
    def route_matched(
        self, input_: InputContract, route: RouteContract, handler: RouteMatchedHandlerContract
    ) -> RouteContract | OutputContract:
        """Take the route onward, or answer with an output and stop the chain."""
