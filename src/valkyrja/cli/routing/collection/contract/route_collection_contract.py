#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.cli.routing.data.cli_routing_data import CliRoutingData
from valkyrja.cli.routing.data.contract.route_contract import RouteContract


class RouteCollectionContract(ABC):
    """The contract for the collection that holds each command."""

    @abstractmethod
    def get_data(self) -> CliRoutingData:
        """Get a data representation of the collection."""

    @abstractmethod
    def set_from_data(self, data: CliRoutingData) -> None:
        """Replace the state of the collection with a data object."""

    @abstractmethod
    def add(self, *commands: RouteContract) -> Self:
        """Add each command to the collection."""

    @abstractmethod
    def get(self, name: str) -> RouteContract:
        """Get the command that carries a given name."""

    @abstractmethod
    def has(self, name: str) -> bool:
        """Get whether the collection holds a command with a given name."""

    @abstractmethod
    def all(self) -> dict[str, RouteContract]:
        """Get every command, keyed by name."""
