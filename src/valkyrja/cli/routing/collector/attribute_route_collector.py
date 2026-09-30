#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import cast, override

from valkyrja.cli.routing.attribute.route import ROUTE_MARKER, RouteMarker
from valkyrja.cli.routing.collector.contract.route_collector_contract import (
    RouteCollectorContract,
)
from valkyrja.cli.routing.data.contract.route_contract import CliHandler, RouteContract
from valkyrja.cli.routing.data.route import Route
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_route_handler_exception import (
    CliRoutingInvalidRouteHandlerException,
)


class AttributeRouteCollector(RouteCollectorContract):
    @override
    def get_routes(self, *classes: type) -> list[RouteContract]:
        routes: list[RouteContract] = []

        for controller in classes:
            routes.extend(self._get_routes_for_class(controller))

        return routes

    def _get_routes_for_class(self, controller: type) -> list[RouteContract]:
        """Read each marked member of one class, and of each class it extends."""
        routes: list[RouteContract] = []
        seen: set[str] = set()

        # `vars` reads one class, so the walk covers what the controller extends.
        for klass in controller.__mro__:
            for name, attribute in vars(klass).items():
                if name in seen:
                    continue

                seen.add(name)
                marker = self._get_marker(attribute)

                if marker is not None:
                    routes.append(self._make_route(marker, self._get_handler(controller, name, attribute)))

        return routes

    @staticmethod
    def _get_marker(attribute: object) -> RouteMarker | None:
        """Read the marker from the attribute, or from the function it wraps.

        `@route` over `@staticmethod` marks the descriptor, and `@route` under it
        marks the function the descriptor wraps, so both places are read.
        """
        for candidate in (attribute, getattr(attribute, "__func__", None)):
            marker = getattr(candidate, ROUTE_MARKER, None)

            if isinstance(marker, RouteMarker):
                return marker

        return None

    @staticmethod
    def _get_handler(controller: type, name: str, attribute: object) -> CliHandler:
        """Get the callable that answers the command.

        A handler takes the container and the arguments alone, so a member that
        also takes an instance or a class cannot answer a command.
        """
        if not isinstance(attribute, staticmethod):
            raise CliRoutingInvalidRouteHandlerException(
                f"`{controller.__qualname__}.{name}` marks a command and is no static method"
            )

        # `staticmethod.__func__` is typed as the wrapped callable, which the
        # marker does not narrow, so the cast states what the decorator guarantees.
        return cast("CliHandler", attribute.__func__)

    @staticmethod
    def _make_route(marker: RouteMarker, handler: CliHandler) -> RouteContract:
        """Build a command from the marker and the function that answers it."""
        return Route(
            name=marker.name,
            description=marker.description,
            handler=handler,
            help_text=marker.help_text,
            route_matched_middleware=list(marker.route_matched_middleware),
            route_dispatched_middleware=list(marker.route_dispatched_middleware),
            throwable_caught_middleware=list(marker.throwable_caught_middleware),
            process_exiting_middleware=list(marker.process_exiting_middleware),
            arguments=list(marker.arguments),
            options=list(marker.options),
        )
