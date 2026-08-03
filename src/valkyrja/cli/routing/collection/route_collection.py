#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Self, override

from valkyrja.cli.routing.collection.contract.route_collection_contract import (
    RouteCollectionContract,
)
from valkyrja.cli.routing.data.cli_routing_data import CliRoutingData, RouteFactory
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_route_name_exception import (
    CliRoutingInvalidRouteNameException,
)


class RouteCollection(RouteCollectionContract):
    """Holds each command, keyed by the name of the command.

    The collection stores a factory for each command, never the command itself.
    `sindri` writes a factory into the generated cache, so the runtime map and
    the cache hold the same shape.
    """

    def __init__(self) -> None:
        self._routes: dict[str, RouteFactory] = {}

    @override
    def get_data(self) -> CliRoutingData:
        return CliRoutingData(routes=dict(self._routes))

    @override
    def set_from_data(self, data: CliRoutingData) -> None:
        self._routes = dict(data.routes)

    @override
    def add(self, *commands: RouteContract) -> Self:
        for command in commands:
            self._routes[command.get_name()] = self._make_factory(command)

        return self

    @override
    def get(self, name: str) -> RouteContract:
        factory = self._routes.get(name)

        if factory is None:
            raise CliRoutingInvalidRouteNameException(f"The route `{name}` was not found.")

        return factory()

    @override
    def has(self, name: str) -> bool:
        return name in self._routes

    @override
    def all(self) -> dict[str, RouteContract]:
        return {name: factory() for name, factory in self._routes.items()}

    @staticmethod
    def _make_factory(command: RouteContract) -> RouteFactory:
        """Wrap a command in a factory, so the map always holds a factory."""
        return lambda: command
