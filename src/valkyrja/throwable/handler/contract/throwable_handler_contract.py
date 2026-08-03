#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod


class ThrowableHandlerContract(ABC):
    """The contract for the handler that catches an unhandled throwable."""

    @abstractmethod
    def enable(self, display_errors: bool = False) -> None:
        """Enable the throwable handler.

        Warning: a handler that displays an error shows the internals of the
        application. Set `display_errors` in development only.
        """
