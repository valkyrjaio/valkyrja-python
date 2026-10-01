#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from copy import copy
from typing import Protocol, Self, override, runtime_checkable

from valkyrja.cli.routing.data.contract.parameter_contract import ParameterContract
from valkyrja.cli.routing.throwable.exception.cli_routing_no_cast_exception import (
    CliRoutingNoCastException,
)
from valkyrja.type.data.cast import Cast


@runtime_checkable
class ValuedParameter(Protocol):
    def get_value(self) -> str:
        """Get the raw value that the user typed."""


class Parameter(ParameterContract):
    def __init__(self, name: str, description: str, cast: Cast | None = None) -> None:
        self._name = name
        self._description = description
        self._cast = cast

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
    def get_values(self) -> list[str]:
        """Get each raw value of the parameter."""

    @staticmethod
    def _get_values_of_parameters(parameters: list[ValuedParameter]) -> list[str]:
        """Read the raw value of each parameter that carries one."""
        return [parameter.get_value() for parameter in parameters]
