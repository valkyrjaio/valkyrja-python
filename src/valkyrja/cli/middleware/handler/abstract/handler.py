#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, override

from valkyrja.cli.middleware.handler.contract.handler_contract import HandlerContract
from valkyrja.container.manager.contract.container_contract import ContainerContract


class Handler(HandlerContract):
    """Walks a chain of middleware, one item at a time.

    The handler holds a binding key for each middleware, never a class. It
    resolves a key through the container as the chain reaches that item, so a
    middleware that the chain never reaches never loads.
    """

    def __init__(self, container: ContainerContract, *middleware: str) -> None:
        self._container = container
        self._middleware: list[str] = list(middleware)
        self._index = 0
        self._next: str | None = None

        self._update_next()

    @override
    def add(self, *middleware: str) -> None:
        # The handler appends, and it never dedupes. A middleware that a caller
        # adds twice runs twice.
        self._middleware = [*self._middleware, *middleware]

        self._update_next()

    def _get_middleware(self, middleware: str) -> Any:
        """Resolve one middleware, and move the chain to the next item."""
        item = self._container.get(middleware)

        self._index += 1

        self._update_next()

        return item

    def _update_next(self) -> None:
        """Point at the middleware that the chain runs next."""
        self._next = self._middleware[self._index] if self._index < len(self._middleware) else None
