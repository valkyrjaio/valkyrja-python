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


class RouteDispatchedHandlerContract(HandlerContract):
    """Runs each middleware for a route that the application dispatched."""

    @abstractmethod
    def route_dispatched(self, input_: InputContract, output: OutputContract, route: RouteContract) -> OutputContract:
        """Run the chain, and get the output that the application writes."""
