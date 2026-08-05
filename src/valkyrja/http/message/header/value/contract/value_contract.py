#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from typing import Self

from valkyrja.http.message.header.value.component.contract.component_contract import (
    ComponentContract,
)


class ValueContract(ABC):
    """The contract for one value of a header.

    PHP also implements `ArrayAccess`, `Countable`, `Iterator`, and
    `JsonSerializable`. Python spells each of those with a dunder method, so a
    concrete value defines `__getitem__`, `__len__`, and `__iter__` instead.
    """

    @abstractmethod
    def __str__(self) -> str:
        """Get the value as a string."""

    @abstractmethod
    def get_components(self) -> list[ComponentContract]:
        """Get each part of the value."""

    @abstractmethod
    def with_components(self, *components: ComponentContract | str) -> Self:
        """Get a copy of the value that carries different parts."""

    @abstractmethod
    def with_added_components(self, *components: ComponentContract | str) -> Self:
        """Get a copy of the value that carries more parts."""
