#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from dataclasses import dataclass, replace
from typing import Self, override

from valkyrja.event.data.contract.listener_contract import ListenerContract, ListenerHandler


@dataclass(frozen=True)
class Listener(ListenerContract):
    """A listener that binds an event id to a handler.

    The dataclass is frozen, so a listener that the collection holds cannot
    change under a caller. Each `with_` method answers with a copy.
    """

    event_id: str
    name: str
    handler: ListenerHandler

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
