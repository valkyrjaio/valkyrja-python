#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import TYPE_CHECKING

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.handler_contract import HandlerContract

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteMatchedHandlerContract(HandlerContract):
    """Runs each middleware for a route that the application matched."""

    @abstractmethod
    def route_matched(self, input_: InputContract, route: RouteContract) -> RouteContract | OutputContract:
        """Run the chain, and get the route onward or an output that stops it."""
