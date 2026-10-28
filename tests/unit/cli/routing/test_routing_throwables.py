#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the exception hierarchy of the Cli Routing and Cli Middleware subcomponents."""

import pytest

from valkyrja.cli.middleware.throwable.contract.cli_middleware_throwable import (
    CliMiddlewareThrowable,
)
from valkyrja.cli.middleware.throwable.exception.abstract.cli_middleware_invalid_argument_exception import (
    CliMiddlewareInvalidArgumentException,
)
from valkyrja.cli.middleware.throwable.exception.abstract.cli_middleware_runtime_exception import (
    CliMiddlewareRuntimeException,
)
from valkyrja.cli.routing.throwable.contract.cli_routing_throwable import CliRoutingThrowable
from valkyrja.cli.routing.throwable.exception.abstract.cli_routing_invalid_argument_exception import (
    CliRoutingInvalidArgumentException,
)
from valkyrja.cli.routing.throwable.exception.abstract.cli_routing_runtime_exception import (
    CliRoutingRuntimeException,
)
from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable
from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable

ABSTRACT_EXCEPTIONS = [
    CliRoutingThrowable,
    CliRoutingRuntimeException,
    CliRoutingInvalidArgumentException,
    CliMiddlewareThrowable,
    CliMiddlewareRuntimeException,
    CliMiddlewareInvalidArgumentException,
]


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_an_abstract_exception_does_not_construct(exception_class: type[ValkyrjaThrowable]) -> None:
    with pytest.raises(TypeError, match="Can't instantiate abstract throwable"):
        exception_class()


@pytest.mark.parametrize("exception_class", ABSTRACT_EXCEPTIONS)
def test_every_exception_narrows_the_cli_throwable(exception_class: type) -> None:
    assert issubclass(exception_class, CliThrowable)


def test_the_routing_bases_extend_the_language_roots() -> None:
    assert issubclass(CliRoutingRuntimeException, RuntimeError)
    assert issubclass(CliRoutingInvalidArgumentException, ValueError)


def test_the_middleware_bases_extend_the_language_roots() -> None:
    assert issubclass(CliMiddlewareRuntimeException, RuntimeError)
    assert issubclass(CliMiddlewareInvalidArgumentException, ValueError)
