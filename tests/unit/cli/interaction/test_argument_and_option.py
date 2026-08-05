#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for Argument and Option."""

from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.enum.option_type import OptionType
from valkyrja.cli.interaction.option.option import Option


def test_an_argument_holds_its_value() -> None:
    assert Argument("first").get_value() == "first"


def test_with_value_returns_a_copy_of_the_argument() -> None:
    argument = Argument("first")

    changed = argument.with_value("second")

    assert changed is not argument
    assert changed.get_value() == "second"
    assert argument.get_value() == "first"


def test_an_option_defaults_to_a_long_form_with_no_value() -> None:
    option = Option("help")

    assert option.get_name() == "help"
    assert option.get_type() is OptionType.LONG
    assert not option.has_value()
    assert option.get_value() == ""


def test_an_option_holds_a_value() -> None:
    assert Option("name", "value").has_value()


def test_with_name_returns_a_copy_of_the_option() -> None:
    option = Option("help")

    changed = option.with_name("version")

    assert changed is not option
    assert changed.get_name() == "version"
    assert option.get_name() == "help"


def test_with_value_returns_a_copy_of_the_option() -> None:
    option = Option("name")

    changed = option.with_value("value")

    assert changed is not option
    assert changed.get_value() == "value"
    assert not option.has_value()


def test_without_value_returns_a_copy_of_the_option() -> None:
    option = Option("name", "value")

    changed = option.without_value()

    assert changed is not option
    assert not changed.has_value()
    assert option.has_value()


def test_with_type_returns_a_copy_of_the_option() -> None:
    option = Option("h")

    changed = option.with_type(OptionType.SHORT)

    assert changed is not option
    assert changed.get_type() is OptionType.SHORT
    assert option.get_type() is OptionType.LONG
