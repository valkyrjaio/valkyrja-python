#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Caster, which applies the cast of a parameter."""

from typing import Any

import pytest

from tests.fixtures.type.string_type_fixture import StringTypeFixture
from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.option.option import Option
from valkyrja.cli.routing.caster.caster import Caster
from valkyrja.cli.routing.data.argument_parameter import ArgumentParameter
from valkyrja.cli.routing.data.option_parameter import OptionParameter
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
)
from valkyrja.type.constant.cast_argument import CastArgument
from valkyrja.type.data.cast import Cast
from valkyrja.type.enum.cast_type import CastType

STRING_TYPE_ID = CastType.STRING.value


def make_type(container: ContainerContract, arguments: dict[str, Any]) -> object:
    # The prefix tells a cast value apart from the raw one that the parameter holds.
    return StringTypeFixture(f"cast:{arguments[CastArgument.VALUE]}")


def make_container() -> Container:
    container = Container()
    container.bind(STRING_TYPE_ID, make_type)

    return container


def test_a_parameter_with_no_cast_answers_with_its_raw_values() -> None:
    parameter = ArgumentParameter("name", "The name").with_arguments(Argument("a"), Argument("b"))

    assert Caster(make_container()).get_cast_values(parameter) == ["a", "b"]


def test_a_cast_that_converts_gives_the_plain_value() -> None:
    parameter = ArgumentParameter("name", "The name", cast=Cast.from_cast_type(CastType.STRING)).with_arguments(
        Argument("a")
    )

    assert Caster(make_container()).get_cast_values(parameter) == ["cast:a"]


def test_a_cast_that_does_not_convert_gives_the_type() -> None:
    parameter = ArgumentParameter(
        "name", "The name", cast=Cast.from_cast_type(CastType.STRING, convert=False)
    ).with_arguments(Argument("a"))

    values: list[Any] = Caster(make_container()).get_cast_values(parameter)

    assert isinstance(values[0], StringTypeFixture)
    assert values[0].as_value() == "cast:a"


def test_an_option_parameter_casts_each_of_its_values() -> None:
    parameter = OptionParameter("name", "The name", cast=Cast.from_cast_type(CastType.STRING)).with_options(
        Option("name", "a"), Option("name", "b")
    )

    assert Caster(make_container()).get_cast_values(parameter) == ["cast:a", "cast:b"]


def test_a_singleton_binding_still_builds_one_type_for_each_value() -> None:
    # The caster asks for a service, so the container never answers from its cache.
    # A singleton would build one type from an empty argument map and reuse it.
    container = Container()
    container.bind_singleton(STRING_TYPE_ID, make_type)
    parameter = OptionParameter("name", "The name", cast=Cast.from_cast_type(CastType.STRING)).with_options(
        Option("name", "a"), Option("name", "b")
    )

    assert Caster(container).get_cast_values(parameter) == ["cast:a", "cast:b"]


def test_a_cast_that_no_binding_names_reports_a_failure() -> None:
    parameter = ArgumentParameter("name", "The name", cast=Cast.from_cast_type(CastType.STRING)).with_arguments(
        Argument("a")
    )

    with pytest.raises(ContainerInvalidReferenceException):
        Caster(Container()).get_cast_values(parameter)
