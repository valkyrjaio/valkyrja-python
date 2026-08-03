#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Any, Self


class ArgumentsCapableEventContract(ABC):
    """The contract for an event that takes the arguments of the dispatch."""

    @abstractmethod
    def set_arguments(self, arguments: dict[str, Any]) -> Self:
        """Set the arguments on the event."""
