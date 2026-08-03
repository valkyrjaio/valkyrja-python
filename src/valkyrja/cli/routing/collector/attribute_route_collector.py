#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

import inspect
from typing import override

from valkyrja.cli.routing.attribute.route import ROUTE_MARKER, RouteMarker
from valkyrja.cli.routing.collector.contract.route_collector_contract import (
    RouteCollectorContract,
)
from valkyrja.cli.routing.data.contract.route_contract import CliHandler, RouteContract
from valkyrja.cli.routing.data.route import Route


class AttributeRouteCollector(RouteCollectorContract):
    """Reads each command that a class marks with `@route`.

    PHP reflects over the `#[Route]` attribute of each method. Python reads the
    marker that the decorator attached, which `inspect.getmembers` finds.
    """

    @override
    def get_routes(self, *classes: type) -> list[RouteContract]:
        routes: list[RouteContract] = []

        for controller in classes:
            routes.extend(self._get_routes_for_class(controller))

        return routes

    def _get_routes_for_class(self, controller: type) -> list[RouteContract]:
        """Read each marked function of one class."""
        routes: list[RouteContract] = []

        for _name, member in inspect.getmembers(controller, inspect.isfunction):
            marker = getattr(member, ROUTE_MARKER, None)

            if isinstance(marker, RouteMarker):
                routes.append(self._make_route(marker, member))

        return routes

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
