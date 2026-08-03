#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class HandlerContract(ABC):
    """The base contract for a handler that runs a chain of middleware.

    PHP types the chain with a generic parameter. Python has no generic on a
    plain method here, so each handler below narrows `add` in its own docstring
    instead. The rule that matters is the same in every port: the handler
    APPENDS each middleware in order, and it never dedupes.
    """

    @abstractmethod
    def add(self, *middleware: str) -> None:
        """Add each middleware to the end of the chain.

        Each middleware is a binding key, never a class. The handler resolves
        the key through the container, and the container resolves a string.

        Warning: the handler never dedupes. A middleware that a caller adds
        twice runs twice. A duplicate is the error of the developer, and the
        generated cache must match what reflection gives.
        """
