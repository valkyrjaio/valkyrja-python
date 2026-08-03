#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class CliRouteProviderContract(ABC):
    """The contract for a provider that gives the commands of a component.

    Each method returns a plain list, and neither method holds a condition.
    `sindri` reads both lists through the abstract syntax tree, and a condition
    is what stops `sindri` from reading them.
    """

    @abstractmethod
    def get_controller_classes(self) -> list[type]:
        """Get each class that declares a command with a marker."""

    @abstractmethod
    def get_routes(self) -> list[RouteContract]:
        """Get each command that the provider declares directly."""
