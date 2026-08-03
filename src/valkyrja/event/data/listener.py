#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.event.data.contract.listener_contract import ListenerContract, ListenerHandler


class Listener(ListenerContract):
    """A listener that binds an event id to a handler.

    Each `with_` method returns a copy, so a listener that the collection holds
    never changes under a caller.
    """

    def __init__(self, event_id: str, name: str, handler: ListenerHandler) -> None:
        self._event_id = event_id
        self._name = name
        self._handler = handler

    @override
    def get_event_id(self) -> str:
        return self._event_id

    @override
    def with_event_id(self, event_id: str) -> Self:
        new = self._copy()
        new._event_id = event_id

        return new

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def with_name(self, name: str) -> Self:
        new = self._copy()
        new._name = name

        return new

    @override
    def get_handler(self) -> ListenerHandler:
        return self._handler

    @override
    def with_handler(self, handler: ListenerHandler) -> Self:
        new = self._copy()
        new._handler = handler

        return new

    def _copy(self) -> Self:
        """Get a shallow copy, which is what PHP's `clone` gives."""
        return copy(self)
