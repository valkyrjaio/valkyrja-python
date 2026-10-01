#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from valkyrja.cli.routing.data.contract.route_contract import RouteContract

type RouteFactory = Callable[[], RouteContract]
"""The collection calls this factory to build a route that the cache holds."""


@dataclass(frozen=True)
class CliRoutingData:
    routes: dict[str, RouteFactory] = field(default_factory=dict)
