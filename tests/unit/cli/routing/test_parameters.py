#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the parameters that a command declares."""

from typing import Any

import pytest

from tests.fixtures.type.string_type_fixture import StringTypeFixture
from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.option.option import Option
from valkyrja.cli.routing.data.argument_parameter import ArgumentParameter
from valkyrja.cli.routing.data.option_parameter import OptionParameter
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.cli.routing.enum.option_mode import OptionMode
from valkyrja.cli.routing.enum.option_value_mode import OptionValueMode
from valkyrja.cli.routing.throwable.exception.cli_routing_no_cast_exception import (
    CliRoutingNoCastException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_parameter_values_validation_exception import (
    CliRoutingParameterValuesValidationException,
)
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.type.data.cast import Cast
from valkyrja.type.enum.cast_type import CastType

STRING_TYPE_ID = CastType.STRING.value


def make_container() -> Container:
    container = Container()
    container.bind(
        STRING_TYPE_ID,
        lambda c, arguments: StringTypeFixture(str(arguments["value"])),
    )

    return container


def test_a_parameter_holds_its_name_and_description() -> None:
    parameter = ArgumentParameter("name", "The name")

    assert parameter.get_name() == "name"
    assert parameter.get_description() == "The name"


def test_the_name_and_description_setters_return_copies() -> None:
    parameter = ArgumentParameter("name", "The name")

    assert parameter.with_name("other").get_name() == "other"
    assert parameter.with_description("Other").get_description() == "Other"
    assert parameter.get_name() == "name"


def test_a_parameter_without_a_cast_raises_when_asked_for_one() -> None:
    with pytest.raises(CliRoutingNoCastException, match="No cast exists"):
        ArgumentParameter("name").get_cast()


def test_the_cast_setters_return_copies() -> None:
    parameter = ArgumentParameter("name")
    cast = Cast.from_cast_type(CastType.STRING)

    with_cast = parameter.with_cast(cast)

    assert with_cast.has_cast()
    assert with_cast.get_cast() is cast
    assert not parameter.has_cast()
    assert not with_cast.without_cast().has_cast()


def test_an_argument_parameter_has_defaults() -> None:
    parameter = ArgumentParameter("name")

    assert parameter.get_mode() is ArgumentMode.REQUIRED
    assert parameter.get_value_mode() is ArgumentValueMode.DEFAULT
    assert parameter.get_arguments() == []
    assert not parameter.has_first_value()


def test_the_argument_parameter_setters_return_copies() -> None:
    parameter = ArgumentParameter("name")

    assert parameter.with_mode(ArgumentMode.OPTIONAL).get_mode() is ArgumentMode.OPTIONAL
    assert parameter.with_value_mode(ArgumentValueMode.ARRAY).get_value_mode() is ArgumentValueMode.ARRAY
    assert parameter.get_mode() is ArgumentMode.REQUIRED


def test_an_argument_parameter_holds_arguments() -> None:
    parameter = ArgumentParameter("name").with_arguments(Argument("a"))

    assert parameter.has_first_value()
    assert [argument.get_value() for argument in parameter.get_arguments()] == ["a"]

    added = parameter.with_added_arguments(Argument("b"))

    assert [argument.get_value() for argument in added.get_arguments()] == ["a", "b"]
    assert len(parameter.get_arguments()) == 1


def test_get_arguments_copies_the_list() -> None:
    parameter = ArgumentParameter("name").with_arguments(Argument("a"))

    parameter.get_arguments().clear()

    assert len(parameter.get_arguments()) == 1


def test_a_parameter_with_no_cast_returns_the_raw_values() -> None:
    parameter = ArgumentParameter("name").with_arguments(Argument("a"), Argument("b"))

    assert parameter.get_cast_values() == ["a", "b"]


def test_a_parameter_with_a_cast_but_no_container_returns_the_raw_values() -> None:
    parameter = ArgumentParameter("name", cast=Cast.from_cast_type(CastType.STRING)).with_arguments(Argument("a"))

    assert parameter.get_cast_values() == ["a"]


def test_a_cast_that_converts_gives_the_plain_value() -> None:
    parameter = ArgumentParameter(
        "name",
        cast=Cast.from_cast_type(CastType.STRING),
        arguments=[Argument("a")],
        container=make_container(),
    )

    assert parameter.get_cast_values() == ["a"]


def test_a_cast_that_does_not_convert_gives_the_type() -> None:
    parameter = ArgumentParameter(
        "name",
        cast=Cast.from_cast_type(CastType.STRING, convert=False),
        arguments=[Argument("a")],
        container=make_container(),
    )

    values: list[Any] = parameter.get_cast_values()

    assert isinstance(values[0], StringTypeFixture)
    assert values[0].as_value() == "a"


def test_an_option_parameter_has_defaults() -> None:
    parameter = OptionParameter("name")

    assert parameter.get_short_names() == []
    assert parameter.get_mode() is OptionMode.OPTIONAL
    assert parameter.get_value_mode() is OptionValueMode.NONE
    assert not parameter.has_value_display_name()
    assert parameter.get_value_display_name() == ""
    assert parameter.get_options() == []
    assert not parameter.has_first_value()


def test_the_option_parameter_setters_return_copies() -> None:
    parameter = OptionParameter("name")

    assert parameter.with_short_names("n").get_short_names() == ["n"]
    assert parameter.with_short_names("n").with_added_short_names("m").get_short_names() == ["n", "m"]
    assert parameter.with_mode(OptionMode.REQUIRED).get_mode() is OptionMode.REQUIRED
    assert parameter.with_value_mode(OptionValueMode.ARRAY).get_value_mode() is OptionValueMode.ARRAY
    assert parameter.with_value_display_name("NAME").has_value_display_name()
    assert parameter.get_short_names() == []
    assert parameter.get_mode() is OptionMode.OPTIONAL


def test_an_option_parameter_holds_options() -> None:
    parameter = OptionParameter("name").with_options(Option("name", "a"))

    assert parameter.has_first_value()

    added = parameter.with_added_options(Option("name", "b"))

    assert len(added.get_options()) == 2
    assert len(parameter.get_options()) == 1


def test_get_short_names_and_options_copy_their_lists() -> None:
    parameter = OptionParameter("name", short_names=["n"], options=[Option("name", "a")])

    parameter.get_short_names().clear()
    parameter.get_options().clear()

    assert len(parameter.get_short_names()) == 1
    assert len(parameter.get_options()) == 1


def test_an_option_parameter_casts_its_values() -> None:
    parameter = OptionParameter(
        "name",
        cast=Cast.from_cast_type(CastType.STRING),
        options=[Option("name", "a")],
        container=make_container(),
    )

    assert parameter.get_cast_values() == ["a"]


def test_an_option_parameter_with_no_cast_returns_the_raw_values() -> None:
    parameter = OptionParameter("name", options=[Option("name", "a")])

    assert parameter.get_cast_values() == ["a"]


def test_the_container_is_the_way_python_resolves_a_cast() -> None:
    """PHP calls `$castType::fromValue()`. Python resolves the key instead."""
    container: ContainerContract = make_container()
    parameter = ArgumentParameter(
        "name",
        cast=Cast(type=STRING_TYPE_ID),
        arguments=[Argument("value")],
        container=container,
    )

    assert parameter.get_cast_values() == ["value"]


def test_a_required_argument_with_no_value_is_not_valid() -> None:
    assert not ArgumentParameter("name", mode=ArgumentMode.REQUIRED).are_values_valid()


def test_a_required_argument_with_a_value_is_valid() -> None:
    parameter = ArgumentParameter("name", mode=ArgumentMode.REQUIRED, arguments=[Argument("a")])

    assert parameter.are_values_valid()


def test_an_optional_argument_with_no_value_is_valid() -> None:
    assert ArgumentParameter("name", mode=ArgumentMode.OPTIONAL).are_values_valid()


def test_a_single_value_argument_rejects_a_second_value() -> None:
    parameter = ArgumentParameter(
        "name",
        mode=ArgumentMode.OPTIONAL,
        value_mode=ArgumentValueMode.DEFAULT,
        arguments=[Argument("a"), Argument("b")],
    )

    assert not parameter.are_values_valid()


def test_an_array_argument_accepts_several_values() -> None:
    parameter = ArgumentParameter(
        "name",
        mode=ArgumentMode.OPTIONAL,
        value_mode=ArgumentValueMode.ARRAY,
        arguments=[Argument("a"), Argument("b")],
    )

    assert parameter.are_values_valid()


def test_validate_values_returns_the_argument_when_valid() -> None:
    parameter = ArgumentParameter("name", mode=ArgumentMode.OPTIONAL)

    assert parameter.validate_values() is parameter


def test_validate_values_raises_for_an_invalid_argument() -> None:
    parameter = ArgumentParameter("name", mode=ArgumentMode.REQUIRED)

    with pytest.raises(CliRoutingParameterValuesValidationException, match="name is invalid"):
        parameter.validate_values()


def test_a_required_option_with_no_value_is_not_valid() -> None:
    assert not OptionParameter("name", mode=OptionMode.REQUIRED).are_values_valid()


def test_an_optional_option_with_no_value_is_valid() -> None:
    assert OptionParameter("name").are_values_valid()


def test_a_single_value_option_rejects_a_second_value() -> None:
    parameter = OptionParameter(
        "name",
        value_mode=OptionValueMode.DEFAULT,
        options=[Option("name", "a"), Option("name", "b")],
    )

    assert not parameter.are_values_valid()


def test_an_option_rejects_a_value_outside_the_valid_values() -> None:
    parameter = OptionParameter("name", options=[Option("name", "other")], valid_values=["a", "b"])

    assert not parameter.are_values_valid()


def test_an_option_accepts_a_value_inside_the_valid_values() -> None:
    parameter = OptionParameter("name", options=[Option("name", "a")], valid_values=["a", "b"])

    assert parameter.are_values_valid()


def test_the_valid_values_setters_return_copies() -> None:
    parameter = OptionParameter("name")

    assert parameter.get_valid_values() == []
    assert parameter.with_valid_values("a").get_valid_values() == ["a"]
    assert parameter.with_valid_values("a").with_added_valid_values("b").get_valid_values() == [
        "a",
        "b",
    ]
    assert parameter.get_valid_values() == []


def test_get_valid_values_copies_the_list() -> None:
    parameter = OptionParameter("name", valid_values=["a"])

    parameter.get_valid_values().clear()

    assert parameter.get_valid_values() == ["a"]


def test_validate_values_raises_for_an_invalid_option() -> None:
    parameter = OptionParameter("name", mode=OptionMode.REQUIRED)

    with pytest.raises(CliRoutingParameterValuesValidationException, match="name is invalid"):
        parameter.validate_values()


def test_validate_values_returns_the_option_when_valid() -> None:
    parameter = OptionParameter("name")

    assert parameter.validate_values() is parameter
