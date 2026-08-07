#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self


class ComponentContract(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """Get the component as a string."""

    @abstractmethod
    def get_token(self) -> str:
        """Get the token of the component."""

    @abstractmethod
    def with_token(self, token: str) -> Self:
        """Get a copy of the component that carries a different token."""

    @abstractmethod
    def get_text(self) -> str:
        """Get the text of the component."""

    @abstractmethod
    def with_text(self, text: str) -> Self:
        """Get a copy of the component that carries a different text."""
