#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CliRoutingServiceId:
    """The binding key for each service of the Cli Routing subcomponent."""

    ROUTER_CONTRACT: Final[str] = "Valkyrja.Cli.Routing.Dispatcher.RouterContract"
    ROUTE_COLLECTION_CONTRACT: Final[str] = "Valkyrja.Cli.Routing.Collection.RouteCollectionContract"
    ROUTE_CONTRACT: Final[str] = "Valkyrja.Cli.Routing.Data.RouteContract"
    CLI_ROUTING_DATA: Final[str] = "Valkyrja.Cli.Routing.Data.CliRoutingData"
