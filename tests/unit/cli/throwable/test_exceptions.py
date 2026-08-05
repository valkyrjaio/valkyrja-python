#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Cli component."""

import pytest

from valkyrja.cli.interaction.throwable.contract.cli_interaction_throwable import (
    CliInteractionThrowable,
)
from valkyrja.cli.interaction.throwable.exception.abstract.cli_interaction_invalid_argument_exception import (
    CliInteractionInvalidArgumentException,
)
from valkyrja.cli.interaction.throwable.exception.abstract.cli_interaction_runtime_exception import (
    CliInteractionRuntimeException,
)
from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable
from valkyrja.cli.throwable.exception.abstract.cli_invalid_argument_exception import (
    CliInvalidArgumentException,
)
from valkyrja.cli.throwable.exception.abstract.cli_runtime_exception import CliRuntimeException
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

ABSTRACT_EXCEPTIONS = [
    CliThrowable,
    CliRuntimeException,
    CliInvalidArgumentException,
    CliInteractionThrowable,
    CliInteractionRuntimeException,
    CliInteractionInvalidArgumentException,
]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


def test_the_cli_bases_extend_the_language_roots() -> None:
    assert issubclass(CliRuntimeException, RuntimeError)
    assert issubclass(CliInvalidArgumentException, ValueError)


def test_the_interaction_throwable_narrows_the_cli_throwable() -> None:
    assert issubclass(CliInteractionThrowable, CliThrowable)
    assert issubclass(CliInteractionRuntimeException, CliInteractionThrowable)
    assert issubclass(CliInteractionInvalidArgumentException, CliInteractionThrowable)
