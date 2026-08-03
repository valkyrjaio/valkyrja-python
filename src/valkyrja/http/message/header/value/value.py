#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.http.message.header.value.component.component import Component
from valkyrja.http.message.header.value.component.contract.component_contract import (
    ComponentContract,
)
from valkyrja.http.message.header.value.contract.value_contract import ValueContract

VALUE_SEPARATOR = ";"
"""What splits one component of a value from the next, when a value is read."""

VALUE_JOINER = "; "
"""What stands between one component of a value and the next, when a value is written."""


class Value(ValueContract):
    """One value of a header, which holds one component or several."""

    def __init__(self, *components: ComponentContract | str) -> None:
        self._components: list[ComponentContract] = self._to_components(components)

    @override
    def __str__(self) -> str:
        written = [str(component).strip() for component in self._components]

        return VALUE_JOINER.join(component for component in written if component != "")

    @override
    def get_components(self) -> list[ComponentContract]:
        return list(self._components)

    @override
    def with_components(self, *components: ComponentContract | str) -> Self:
        new = copy(self)
        new._components = self._to_components(components)

        return new

    @override
    def with_added_components(self, *components: ComponentContract | str) -> Self:
        new = copy(self)
        new._components = [*self._components, *self._to_components(components)]

        return new

    @staticmethod
    def _to_components(
        components: tuple[ComponentContract | str, ...],
    ) -> list[ComponentContract]:
        """Take a component as it is, and build one from a string."""
        return [
            component if isinstance(component, ComponentContract) else Component.from_string(component)
            for component in components
        ]

    @staticmethod
    def from_string(value: str) -> Value:
        """Build a value from the string that a header carries."""
        return Value(*[part for part in value.split(VALUE_SEPARATOR) if part.strip() != ""])
