#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Any, Self, override

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.routing.data.abstract.parameter import Parameter, ValuedParameter
from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.type.data.cast import Cast


class ArgumentParameter(Parameter, ArgumentParameterContract):
    """One positional parameter that a command declares."""

    def __init__(
        self,
        name: str,
        description: str = "",
        cast: Cast | None = None,
        mode: ArgumentMode = ArgumentMode.REQUIRED,
        value_mode: ArgumentValueMode = ArgumentValueMode.DEFAULT,
        arguments: list[ArgumentContract] | None = None,
        container: ContainerContract | None = None,
    ) -> None:
        super().__init__(name, description, cast, container)

        self._mode = mode
        self._value_mode = value_mode
        self._arguments: list[ArgumentContract] = list(arguments) if arguments is not None else []

    @override
    def get_mode(self) -> ArgumentMode:
        return self._mode

    @override
    def with_mode(self, mode: ArgumentMode) -> Self:
        new = self._copy()
        new._mode = mode

        return new

    @override
    def get_value_mode(self) -> ArgumentValueMode:
        return self._value_mode

    @override
    def with_value_mode(self, value_mode: ArgumentValueMode) -> Self:
        new = self._copy()
        new._value_mode = value_mode

        return new

    @override
    def get_arguments(self) -> list[ArgumentContract]:
        return list(self._arguments)

    @override
    def with_arguments(self, *arguments: ArgumentContract) -> Self:
        new = self._copy()
        new._arguments = list(arguments)

        return new

    @override
    def with_added_arguments(self, *arguments: ArgumentContract) -> Self:
        new = self._copy()
        new._arguments = [*new._arguments, *arguments]

        return new

    @override
    def get_cast_values(self) -> list[Any]:
        return self._get_cast_values_for_parameters(list[ValuedParameter](self._arguments))

    @override
    def has_first_value(self) -> bool:
        return self._arguments != []

    def _copy(self) -> Self:
        """Get a copy that holds its own argument list."""
        new = copy(self)
        new._arguments = list(self._arguments)

        return new
