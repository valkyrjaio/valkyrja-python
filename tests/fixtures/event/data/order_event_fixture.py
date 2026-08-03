#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.event.contract.event_contract import EventContract

ORDER_PLACED_ID = "Valkyrja.Tests.Fixtures.Event.OrderPlacedFixture"
ORDER_SHIPPED_ID = "Valkyrja.Tests.Fixtures.Event.OrderShippedFixture"


@final
class OrderPlacedFixture(EventContract):
    """An event that a test dispatches."""

    @override
    def get_event_id(self) -> str:
        return ORDER_PLACED_ID


@final
class OrderShippedFixture(EventContract):
    """A second event, so a test reads one event apart from the other."""

    @override
    def get_event_id(self) -> str:
        return ORDER_SHIPPED_ID
