#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.cli.interaction.argument.contract.argument_contract import ArgumentContract
from valkyrja.cli.interaction.argument.factory.argument_factory import ArgumentFactory
from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract
from valkyrja.cli.interaction.option.factory.option_factory import OptionFactory

END_OF_OPTIONS = "--"
"""The POSIX marker that ends the options and starts the operands."""

STANDARD_INPUT = "-"
"""A lone dash names standard input, so it is an operand and never an option."""


@final
class InputFactory:
    """Builds an input from what the user typed."""

    @staticmethod
    def from_globals(args: list[str], application_name: str, command_name: str) -> InputContract:
        """Build an input from the arguments of the command line."""
        return InputFactory.input_with_properties(Input(), args, application_name, command_name)

    @staticmethod
    def input_with_properties(
        input_: InputContract, args: list[str], application_name: str, command_name: str
    ) -> InputContract:
        """Read each item of the command line onto an input."""
        arguments: list[ArgumentContract] = []
        options: list[OptionContract] = []
        end_of_options = False

        for key, arg in enumerate(args):
            if key == 0:
                application_name = arg
            elif not end_of_options and arg == END_OF_OPTIONS:
                # The marker itself is consumed. Every item after it is an
                # operand, however many dashes it starts with, so a second `--`
                # is an ordinary operand.
                end_of_options = True
            elif not end_of_options and arg != STANDARD_INPUT and arg.startswith("-"):
                options = [*options, *OptionFactory.from_arg(arg)]
            elif key == 1:
                command_name = arg
            else:
                arguments.append(ArgumentFactory.from_arg(arg))

        return (
            input_.with_caller(application_name)
            .with_command_name(command_name)
            .with_arguments(*arguments)
            .with_options(*options)
        )
