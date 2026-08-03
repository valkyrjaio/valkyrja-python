#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for Input and the factories that build one."""

import pytest

from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.argument.factory.argument_factory import ArgumentFactory
from valkyrja.cli.interaction.enum.option_type import OptionType
from valkyrja.cli.interaction.input.factory.input_factory import InputFactory
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.option.factory.option_factory import OptionFactory
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


def test_a_new_input_has_defaults() -> None:
    input_ = Input()

    assert input_.get_caller() == "valkyrja"
    assert input_.get_command_name() == "list"
    assert input_.get_arguments() == []
    assert input_.get_options() == []


def test_with_caller_and_command_name_return_copies() -> None:
    input_ = Input()

    assert input_.with_caller("app").get_caller() == "app"
    assert input_.with_command_name("run").get_command_name() == "run"
    assert input_.get_caller() == "valkyrja"


def test_arguments_round_trip() -> None:
    input_ = Input().with_arguments(Argument("a"), Argument("b"))

    assert [argument.get_value() for argument in input_.get_arguments()] == ["a", "b"]

    added = input_.with_added_argument(Argument("c"))

    assert len(added.get_arguments()) == 3
    assert len(input_.get_arguments()) == 2

    assert [a.get_value() for a in added.without_argument("b").get_arguments()] == ["a", "c"]
    assert added.without_arguments().get_arguments() == []


def test_get_arguments_copies_the_list() -> None:
    input_ = Input().with_arguments(Argument("a"))

    input_.get_arguments().clear()

    assert len(input_.get_arguments()) == 1


def test_options_round_trip() -> None:
    input_ = Input().with_options(Option("help"), Option("v", type_=OptionType.SHORT))

    assert input_.has_option("help")
    assert not input_.has_option("missing")
    assert [option.get_name() for option in input_.get_option("help")] == ["help"]

    added = input_.with_added_option(Option("quiet"))

    assert len(added.get_options()) == 3
    assert len(input_.get_options()) == 2
    assert not added.without_option("help").has_option("help")
    assert added.without_options().get_options() == []


def test_get_options_copies_the_list() -> None:
    input_ = Input().with_options(Option("help"))

    input_.get_options().clear()

    assert len(input_.get_options()) == 1


def test_the_argument_factory_builds_an_argument() -> None:
    assert ArgumentFactory.from_arg("value").get_value() == "value"


def test_the_option_factory_reads_a_long_option() -> None:
    options = OptionFactory.from_arg("--help")

    assert len(options) == 1
    assert options[0].get_name() == "help"
    assert options[0].get_type() is OptionType.LONG
    assert not options[0].has_value()


def test_the_option_factory_reads_a_value() -> None:
    options = OptionFactory.from_arg("--name=value")

    assert options[0].get_name() == "name"
    assert options[0].get_value() == "value"


def test_the_option_factory_splits_on_the_first_equals_only() -> None:
    assert OptionFactory.from_arg("--expr=a=b")[0].get_value() == "a=b"


def test_the_option_factory_reads_a_short_option() -> None:
    options = OptionFactory.from_arg("-h")

    assert options[0].get_name() == "h"
    assert options[0].get_type() is OptionType.SHORT


def test_the_option_factory_splits_combined_short_options() -> None:
    options = OptionFactory.from_arg("-abc")

    assert [option.get_name() for option in options] == ["a", "b", "c"]
    assert all(option.get_type() is OptionType.SHORT for option in options)


def test_a_short_option_with_a_value_stays_one_option() -> None:
    options = OptionFactory.from_arg("-n=value")

    assert len(options) == 1
    assert options[0].get_name() == "n"


@pytest.mark.parametrize("arg", ["plain", "-"])
def test_the_option_factory_rejects_an_item_that_names_no_option(arg: str) -> None:
    with pytest.raises(CliInteractionInvalidOptionNameException, match="Invalid option"):
        OptionFactory.from_arg(arg)


def test_the_option_factory_rejects_an_option_with_no_name() -> None:
    with pytest.raises(CliInteractionInvalidEmptyValueException, match="requires a name"):
        OptionFactory.from_arg("--=value")


def test_the_option_factory_rejects_a_value_on_combined_short_options() -> None:
    with pytest.raises(CliInteractionInvalidNonEmptyValueException, match="cannot have a value"):
        OptionFactory.from_arg("-abc=value")


def test_the_input_factory_reads_the_caller_and_the_command() -> None:
    input_ = InputFactory.from_globals(["bin/valkyrja", "run"], "app", "list")

    assert input_.get_caller() == "bin/valkyrja"
    assert input_.get_command_name() == "run"


def test_the_input_factory_keeps_the_defaults_for_an_empty_command_line() -> None:
    input_ = InputFactory.from_globals([], "app", "list")

    assert input_.get_caller() == "app"
    assert input_.get_command_name() == "list"


def test_the_input_factory_reads_options_and_arguments() -> None:
    input_ = InputFactory.from_globals(["bin", "run", "--verbose", "first", "-a", "second"], "app", "list")

    assert input_.has_option("verbose")
    assert input_.has_option("a")
    assert [argument.get_value() for argument in input_.get_arguments()] == ["first", "second"]


def test_an_option_at_index_one_leaves_the_command_name_at_its_default() -> None:
    """The parser reads the command name at index 1 alone.

    An option at index 1 takes that place, so the item after it becomes an
    argument and the command name keeps the default. PHP behaves the same way.
    """
    input_ = InputFactory.from_globals(["bin", "--verbose", "run"], "app", "list")

    assert input_.has_option("verbose")
    assert input_.get_command_name() == "list"
    assert [argument.get_value() for argument in input_.get_arguments()] == ["run"]


def test_the_end_of_options_marker_makes_every_later_item_an_argument() -> None:
    input_ = InputFactory.from_globals(["bin", "run", "--", "--not-an-option", "--"], "app", "list")

    assert not input_.has_option("not-an-option")
    assert [argument.get_value() for argument in input_.get_arguments()] == [
        "--not-an-option",
        "--",
    ]


def test_a_lone_dash_is_an_argument() -> None:
    input_ = InputFactory.from_globals(["bin", "run", "-"], "app", "list")

    assert [argument.get_value() for argument in input_.get_arguments()] == ["-"]
