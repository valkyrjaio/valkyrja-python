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
    ROUTER_CONTRACT: Final[str] = "valkyrja.cli.routing.dispatcher.RouterContract"
    ROUTE_COLLECTION_CONTRACT: Final[str] = "valkyrja.cli.routing.collection.RouteCollectionContract"
    ROUTE_CONTRACT: Final[str] = "valkyrja.cli.routing.data.RouteContract"
    CLI_ROUTING_DATA: Final[str] = "valkyrja.cli.routing.data.CliRoutingData"
