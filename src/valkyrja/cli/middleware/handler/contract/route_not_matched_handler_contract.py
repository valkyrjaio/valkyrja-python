#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.handler.contract.handler_contract import HandlerContract


class RouteNotMatchedHandlerContract(HandlerContract):
    """Runs each middleware for a route that the application did not match."""

    @abstractmethod
    def route_not_matched(self, input_: InputContract, output: OutputContract) -> OutputContract:
        """Run the chain, and get the output that the application writes."""
