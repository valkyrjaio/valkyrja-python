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
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract


class Input(InputContract):
    """What the user typed on the command line."""

    def __init__(
        self,
        caller: str = "valkyrja",
        command_name: str = "list",
        arguments: list[ArgumentContract] | None = None,
        options: list[OptionContract] | None = None,
    ) -> None:
        self._caller = caller
        self._command_name = command_name
        self._arguments: list[ArgumentContract] = list(arguments) if arguments is not None else []
        self._options: list[OptionContract] = list(options) if options is not None else []

    @override
    def get_caller(self) -> str:
        return self._caller

    @override
    def with_caller(self, caller: str) -> Self:
        new = self._copy()
        new._caller = caller

        return new

    @override
    def get_command_name(self) -> str:
        return self._command_name

    @override
    def with_command_name(self, command_name: str) -> Self:
        new = self._copy()
        new._command_name = command_name

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
    def with_added_argument(self, argument: ArgumentContract) -> Self:
        new = self._copy()
        new._arguments.append(argument)

        return new

    @override
    def without_argument(self, value: str) -> Self:
        new = self._copy()
        new._arguments = [argument for argument in new._arguments if argument.get_value() != value]

        return new

    @override
    def without_arguments(self) -> Self:
        new = self._copy()
        new._arguments = []

        return new

    @override
    def get_options(self) -> list[OptionContract]:
        return list(self._options)

    @override
    def get_option(self, name: str) -> list[OptionContract]:
        return [option for option in self._options if option.get_name() == name]

    @override
    def has_option(self, name: str) -> bool:
        return self.get_option(name) != []

    @override
    def with_options(self, *options: OptionContract) -> Self:
        new = self._copy()
        new._options = list(options)

        return new

    @override
    def with_added_option(self, option: OptionContract) -> Self:
        new = self._copy()
        new._options.append(option)

        return new

    @override
    def without_option(self, name: str) -> Self:
        new = self._copy()
        new._options = [option for option in new._options if option.get_name() != name]

        return new

    @override
    def without_options(self) -> Self:
        new = self._copy()
        new._options = []

        return new

    def _copy(self) -> Self:
        """Get a copy that holds its own argument list and option list."""
        new = copy(self)
        new._arguments = list(self._arguments)
        new._options = list(self._options)

        return new
