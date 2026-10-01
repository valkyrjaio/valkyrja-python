#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the pieces of the Type component that the Cli routing parameters need."""

import dataclasses
import inspect

import pytest

from valkyrja.type.constant.cast_argument import CastArgument
from valkyrja.type.contract.type_contract import TypeContract
from valkyrja.type.data.cast import Cast
from valkyrja.type.enum.cast_type import CastType
from valkyrja.type.throwable.contract.type_throwable import TypeThrowable
from valkyrja.type.throwable.exception.abstract.type_invalid_argument_exception import (
    TypeInvalidArgumentException,
)
from valkyrja.type.throwable.exception.abstract.type_runtime_exception import TypeRuntimeException


def test_the_type_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        TypeContract()  # type: ignore[abstract]


def test_the_type_contract_declares_an_abstract_method() -> None:
    assert inspect.isabstract(TypeContract)


def test_every_cast_type_names_a_type_by_string() -> None:
    for cast_type in CastType:
        assert isinstance(cast_type.value, str)
        assert cast_type.value.startswith("valkyrja.type.")


def test_cast_type_holds_every_member_that_php_holds() -> None:
    assert len(CastType) == 12


def test_a_cast_defaults_to_a_converting_single_value() -> None:
    cast = Cast(type_=CastType.STRING.value)

    assert cast.type_ == "valkyrja.type.string.StringT"
    assert cast.convert
    assert not cast.is_array


def test_from_cast_type_builds_a_cast() -> None:
    cast = Cast.from_cast_type(CastType.INT, convert=False, is_array=True)

    assert cast.type_ == "valkyrja.type.int.IntT"
    assert not cast.convert
    assert cast.is_array


def test_a_cast_is_frozen() -> None:
    cast = Cast(type_=CastType.BOOL.value)

    with pytest.raises(dataclasses.FrozenInstanceError):
        cast.type_ = "other"  # type: ignore[misc]


def test_the_type_throwable_bases_do_not_construct() -> None:
    for exception_class in (TypeThrowable, TypeRuntimeException, TypeInvalidArgumentException):
        with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
            exception_class()


def test_the_type_bases_extend_the_language_roots() -> None:
    assert issubclass(TypeRuntimeException, RuntimeError)
    assert issubclass(TypeInvalidArgumentException, ValueError)
    assert issubclass(TypeRuntimeException, TypeThrowable)
    assert issubclass(TypeInvalidArgumentException, TypeThrowable)


def test_the_cast_argument_names_the_value() -> None:
    # The caster passes the raw value under this name, so the type reads it.
    assert CastArgument.VALUE == "value"
