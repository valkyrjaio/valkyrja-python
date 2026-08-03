#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, Self, final, override

from valkyrja.event.contract.arguments_capable_event_contract import ArgumentsCapableEventContract
from valkyrja.event.contract.dispatch_collectable_event_contract import (
    DispatchCollectableEventContract,
)

EVENT_ID = "Valkyrja.Tests.Fixtures.Event.EventFixture"


@final
class EventFixture(ArgumentsCapableEventContract, DispatchCollectableEventContract):
    """An event that takes the arguments and keeps what each listener returns."""

    def __init__(self, event_id: str = EVENT_ID) -> None:
        self.event_id = event_id
        self.arguments: dict[str, Any] = {}
        self.dispatches: list[Any] = []

    @override
    def get_event_id(self) -> str:
        return self.event_id

    @override
    def set_arguments(self, arguments: dict[str, Any]) -> Self:
        self.arguments = arguments

        return self

    @override
    def add_dispatch(self, dispatch: Any) -> None:
        self.dispatches.append(dispatch)

    @override
    def get_dispatches(self) -> list[Any]:
        return self.dispatches
