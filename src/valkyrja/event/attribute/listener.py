#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar

Function = TypeVar("Function", bound=Callable[..., Any])
"""The decorator returns the function it received, with its type intact."""

LISTENER_MARKER = "_valkyrja_event_listeners"
"""The attribute that `@listener` attaches to a function."""


@dataclass(frozen=True)
class ListenerMarker:
    event_id: str
    name: str


def listener(event_id: str, name: str) -> Callable[[Function], Function]:
    """Mark a function as a listener of one event.

    Warning: the decorator records metadata and nothing else. It never registers
    the listener. The collector reads the marker at bootstrap, and `sindri` reads
    it from the source, so a cached application never runs the collector.

    The decorated function is the handler, so the marker holds no reference to a
    callable. A reference would name a binding that the module has not built yet,
    and the import would fail.
    """

    def decorator(function: Function) -> Function:
        # A function listens to several events when the decorator is stacked, and
        # a decorator under another runs first, so the newest marker goes first.
        markers: tuple[ListenerMarker, ...] = getattr(function, LISTENER_MARKER, ())
        setattr(function, LISTENER_MARKER, (ListenerMarker(event_id=event_id, name=name), *markers))

        return function

    return decorator
