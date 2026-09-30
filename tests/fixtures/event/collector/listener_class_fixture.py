#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final

from tests.fixtures.event.data.order_event_fixture import ORDER_PLACED_ID, ORDER_SHIPPED_ID
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.attribute.listener import listener


@final
class ListenerClassFixture:
    """A class whose marked functions a collector reads."""

    @staticmethod
    @listener(ORDER_PLACED_ID, "fixture.order_placed")
    def on_order_placed(container: ContainerContract, arguments: dict[str, Any]) -> str:
        return "placed"

    @staticmethod
    @listener(ORDER_PLACED_ID, "fixture.both.placed")
    @listener(ORDER_SHIPPED_ID, "fixture.both.shipped")
    def on_either(container: ContainerContract, arguments: dict[str, Any]) -> str:
        return "either"

    @staticmethod
    def not_a_listener(container: ContainerContract, arguments: dict[str, Any]) -> str:
        return "no"


@final
class UnmarkedClassFixture:
    """A class that marks no function, so a collector reads none."""

    @staticmethod
    def plain(container: ContainerContract, arguments: dict[str, Any]) -> str:
        return "plain"
