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
from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouterContract(ABC):
    """The contract for the router that answers a command."""

    @abstractmethod
    def dispatch(self, input_: InputContract) -> OutputContract:
        """Match a command to the input, then answer it."""

    @abstractmethod
    def dispatch_route(self, input_: InputContract, route: RouteContract) -> OutputContract:
        """Answer one command."""
