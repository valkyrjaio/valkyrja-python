#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Cli Server subcomponent."""

import pytest

from valkyrja.cli.server.throwable.contract.cli_server_throwable import CliServerThrowable
from valkyrja.cli.server.throwable.exception.abstract.cli_server_invalid_argument_exception import (
    CliServerInvalidArgumentException,
)
from valkyrja.cli.server.throwable.exception.abstract.cli_server_runtime_exception import (
    CliServerRuntimeException,
)
from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

ABSTRACT_EXCEPTIONS = [
    CliServerThrowable,
    CliServerRuntimeException,
    CliServerInvalidArgumentException,
]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_every_exception_narrows_the_cli_throwable(exception_class: type) -> None:
    assert issubclass(exception_class, CliThrowable)


def test_the_bases_extend_the_language_roots() -> None:
    assert issubclass(CliServerRuntimeException, RuntimeError)
    assert issubclass(CliServerInvalidArgumentException, ValueError)
