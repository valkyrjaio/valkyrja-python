#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from copy import copy
from typing import Any, Protocol, Self, override, runtime_checkable
from typing import cast as type_cast

from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.cli.routing.throwable.exception.cli_routing_no_cast_exception import (
    CliRoutingNoCastException,
)
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.type.contract.type_contract import TypeContract
from valkyrja.type.data.cast import Cast


@runtime_checkable
class ValuedParameter(Protocol):
    """A thing that carries one raw value, which an argument and an option both do."""

    def get_value(self) -> str:
        """Get the raw value that the user typed."""


class Parameter(ParameterContract):
    """The shared state of a parameter that a command declares."""

    def __init__(
        self,
        name: str,
        description: str,
        cast: Cast | None = None,
        container: ContainerContract | None = None,
    ) -> None:
        self._name = name
        self._description = description
        self._cast = cast
        self._container = container

    @override
    def get_name(self) -> str:
        return self._name

    @override
    def with_name(self, name: str) -> Self:
        new = copy(self)
        new._name = name

        return new

    @override
    def has_cast(self) -> bool:
        return self._cast is not None

    @override
    def get_cast(self) -> Cast:
        if self._cast is None:
            raise CliRoutingNoCastException("No cast exists")

        return self._cast

    @override
    def with_cast(self, cast: Cast) -> Self:
        new = copy(self)
        new._cast = cast

        return new

    @override
    def without_cast(self) -> Self:
        new = copy(self)
        new._cast = None

        return new

    @override
    def get_description(self) -> str:
        return self._description

    @override
    def with_description(self, description: str) -> Self:
        new = copy(self)
        new._description = description

        return new

    @abstractmethod
    @override
    def get_cast_values(self) -> list[Any]:
        """Get each value of the parameter, with the cast applied to it."""

    def _get_cast_values_for_parameters(self, parameters: list[ValuedParameter]) -> list[Any]:
        """Apply the cast of this parameter to each raw value.

        PHP writes `$castType::fromValue($value)`, a static call on a variable
        class. Python cannot make that call, so the cast names a binding key and
        the container builds the type. The event dispatcher resolves an event id
        the same way, and Go resolves both that way.

        The method returns the raw value where the parameter has no cast, or
        where it has no container to resolve the cast with.
        """
        cast = self._cast
        container = self._container

        if cast is None or container is None:
            return [parameter.get_value() for parameter in parameters]

        values: list[Any] = []

        for parameter in parameters:
            value = type_cast("TypeContract", container.get(cast.type, {"value": parameter.get_value()}))

            values.append(value.as_value() if cast.convert else value)

        return values
