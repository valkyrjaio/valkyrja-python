#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.cli.interaction.enum.option_type import OptionType
from valkyrja.cli.interaction.option.contract.option_contract import OptionContract
from valkyrja.cli.interaction.option.option import Option
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_empty_value_exception import (
    CliInteractionInvalidEmptyValueException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_non_empty_value_exception import (
    CliInteractionInvalidNonEmptyValueException,
)
from valkyrja.cli.interaction.throwable.exception.cli_interaction_invalid_option_name_exception import (
    CliInteractionInvalidOptionNameException,
)


@final
class OptionFactory:
    """Builds each option that one item of the command line names."""

    @staticmethod
    def from_arg(arg: str) -> list[OptionContract]:
        """Build each option that an item of the command line names.

        One item names several options when it combines short options, so
        `-abc` gives three options.
        """
        OptionFactory._validate_arg_is_option(arg)

        type_ = OptionFactory._get_option_type(arg)
        # Split on the first `=` only, so a value that holds one survives whole.
        # `--expr=a=b` gives `a=b`, never `a`.
        parts = arg.split("=", 1)
        name = parts[0].strip("- ")
        value = parts[1] if len(parts) > 1 else ""

        OptionFactory._validate_non_empty_name(name)

        if type_ is OptionType.SHORT and len(name) > 1:
            OptionFactory._validate_value_is_empty(value)

            return OptionFactory._split_combined_short_options(type_, name)

        return [Option(name=name, value=value, type_=type_)]

    @staticmethod
    def _get_option_type(arg: str) -> OptionType:
        """Get whether the item names a long option or a short one."""
        return OptionType.LONG if arg.startswith("--") else OptionType.SHORT

    @staticmethod
    def _split_combined_short_options(type_: OptionType, name: str) -> list[OptionContract]:
        """Split `-abc` into one option for each letter."""
        return [Option(name=letter, value="", type_=type_) for letter in name]

    @staticmethod
    def _validate_arg_is_option(arg: str) -> None:
        """Report an item that names no option."""
        if not arg.startswith("-") or arg == "-":
            raise CliInteractionInvalidOptionNameException(f"Invalid option provided: `{arg}`")

    @staticmethod
    def _validate_non_empty_name(name: str) -> None:
        """Report an option with no name."""
        if name == "":
            raise CliInteractionInvalidEmptyValueException("An option requires a name")

    @staticmethod
    def _validate_value_is_empty(value: str) -> None:
        """Report a value on a set of combined short options."""
        if value != "":
            raise CliInteractionInvalidNonEmptyValueException("Combined short options cannot have a value")
