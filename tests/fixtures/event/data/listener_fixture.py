#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from dataclasses import dataclass, replace
from typing import Any, Self, final, override

from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.event.data.contract.listener_contract import ListenerContract, ListenerHandler

EVENT_ID = "tests.fixtures.event.Event"
LISTENER_NAME = "tests.fixtures.event.Listener"


def handle(container: ContainerContract, arguments: dict[str, Any]) -> Any:
    """Return the arguments, so a test reads what the dispatcher passed."""
    return arguments


@final
@dataclass(frozen=True)
class ListenerFixture(ListenerContract):
    """An immutable listener, because each `with_` method returns a copy."""

    event_id: str = EVENT_ID
    name: str = LISTENER_NAME
    handler: ListenerHandler = handle

    @override
    def get_event_id(self) -> str:
        return self.event_id

    @override
    def with_event_id(self, event_id: str) -> Self:
        return replace(self, event_id=event_id)

    @override
    def get_name(self) -> str:
        return self.name

    @override
    def with_name(self, name: str) -> Self:
        return replace(self, name=name)

    @override
    def get_handler(self) -> ListenerHandler:
        return self.handler

    @override
    def with_handler(self, handler: ListenerHandler) -> Self:
        return replace(self, handler=handler)
