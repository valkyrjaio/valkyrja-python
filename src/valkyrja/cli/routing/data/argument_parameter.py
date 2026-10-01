#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Self, override

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.routing.data.abstract.parameter import Parameter, ValuedParameter
from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.cli.routing.throwable.exception.cli_routing_argument_values_validation_exception import (
    CliRoutingArgumentValuesValidationException,
)
from valkyrja.type.data.cast import Cast


class ArgumentParameter(Parameter, ArgumentParameterContract):
    def __init__(
        self,
        name: str,
        description: str,
        cast: Cast | None = None,
        mode: ArgumentMode = ArgumentMode.OPTIONAL,
        value_mode: ArgumentValueMode = ArgumentValueMode.DEFAULT,
        arguments: list[ArgumentContract] | None = None,
    ) -> None:
        super().__init__(name, description, cast)

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
    def get_values(self) -> list[str]:
        return self._get_values_of_parameters(list[ValuedParameter](self._arguments))

    @override
    def is_provided(self) -> bool:
        return self._arguments != []

    @override
    def has_first_value(self) -> bool:
        return self.get_first_value() != ""

    @override
    def get_first_value(self) -> str:
        if self._arguments == []:
            return ""

        return self._arguments[0].get_value()

    @override
    def are_values_valid(self) -> bool:
        valid = True

        if self._mode is ArgumentMode.REQUIRED:
            valid = self._arguments != []

        if self._value_mode is ArgumentValueMode.DEFAULT:
            valid = valid and len(self._arguments) <= 1

        return valid

    @override
    def validate_values(self) -> Self:
        if not self.are_values_valid():
            raise CliRoutingArgumentValuesValidationException(f"{self._name} is invalid")

        return self

    def _copy(self) -> Self:
        """Get a copy that holds its own argument list."""
        new = copy(self)
        new._arguments = list(self._arguments)

        return new
