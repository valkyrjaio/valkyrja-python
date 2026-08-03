#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Self

from valkyrja.container.manager.contract.container_contract import ContainerContract

type ListenerHandler = Callable[[ContainerContract, dict[str, Any]], Any]
"""The dispatcher calls this handler when the event that the listener names fires."""


class ListenerContract(ABC):
    """The contract for a listener, which binds an event id to a handler."""

    @abstractmethod
    def get_event_id(self) -> str:
        """Get the id of the event that the listener waits for."""

    @abstractmethod
    def with_event_id(self, event_id: str) -> Self:
        """Get a copy of the listener that waits for a different event id."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the listener, which is unique."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the listener that carries a different name."""

    @abstractmethod
    def get_handler(self) -> ListenerHandler:
        """Get the handler that the dispatcher calls."""

    @abstractmethod
    def with_handler(self, handler: ListenerHandler) -> Self:
        """Get a copy of the listener that carries a different handler."""
