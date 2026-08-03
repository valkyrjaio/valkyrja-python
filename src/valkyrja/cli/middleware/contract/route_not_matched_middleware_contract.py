#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)


class RouteNotMatchedMiddlewareContract(ABC):
    """Runs after the application matches no route."""

    @abstractmethod
    def route_not_matched(
        self, input_: InputContract, output: OutputContract, handler: RouteNotMatchedHandlerContract
    ) -> OutputContract:
        """Get the output that the application writes when it matches no route."""
