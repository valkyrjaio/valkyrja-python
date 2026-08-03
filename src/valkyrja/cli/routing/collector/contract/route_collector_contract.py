#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteCollectorContract(ABC):
    """The contract for the collector that reads a command from a class."""

    @abstractmethod
    def get_routes(self, *classes: type) -> list[RouteContract]:
        """Get each command that the given classes declare."""
