#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.event.contract.stoppable_event_contract import StoppableEventContract

STOPPABLE_EVENT_ID = "Valkyrja.Tests.Fixtures.Event.StoppableEventFixture"


@final
class StoppableEventFixture(StoppableEventContract):
    """An event that stops the dispatcher once a test calls `stop`."""

    def __init__(self, event_id: str = STOPPABLE_EVENT_ID) -> None:
        self.event_id = event_id
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True

    @override
    def get_event_id(self) -> str:
        return self.event_id

    @override
    def is_propagation_stopped(self) -> bool:
        return self.stopped
