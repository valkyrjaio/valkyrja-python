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
from valkyrja.cli.middleware.handler.contract.route_dispatched_handler_contract import (
    RouteDispatchedHandlerContract,
)

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteDispatchedMiddlewareContract(ABC):
    """Runs after the application dispatches a route."""

    @abstractmethod
    def route_dispatched(
        self,
        input_: InputContract,
        output: OutputContract,
        route: RouteContract,
        handler: RouteDispatchedHandlerContract,
    ) -> OutputContract:
        """Get the output that the application writes after it dispatches the route."""
