#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.event.contract.stoppable_event_contract import StoppableEventContract


@final
class StoppableEventFixture(StoppableEventContract):
    """An event that stops the dispatcher once a test calls `stop`."""

    def __init__(self) -> None:
        self.stopped = False

    def stop(self) -> None:
        self.stopped = True

    @override
    def is_propagation_stopped(self) -> bool:
        return self.stopped
