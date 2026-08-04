#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts of the Cli Middleware subcomponent.

The implementation pass fills each contract in. Each test pins that the contract
is abstract, so a later change cannot make it constructible without a failure.
"""

import inspect

import pytest

from valkyrja.cli.middleware.constant.cli_middleware_service_id import CliMiddlewareServiceId
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.process_exiting_middleware_contract import (
    ProcessExitingMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_dispatched_middleware_contract import (
    RouteDispatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_matched_middleware_contract import (
    RouteMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_not_matched_middleware_contract import (
    RouteNotMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.handler_contract import HandlerContract
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_dispatched_handler_contract import (
    RouteDispatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)

MIDDLEWARE_CONTRACTS: list[type] = [
    InputReceivedMiddlewareContract,
    RouteMatchedMiddlewareContract,
    RouteNotMatchedMiddlewareContract,
    RouteDispatchedMiddlewareContract,
    ThrowableCaughtMiddlewareContract,
    ProcessExitingMiddlewareContract,
]

HANDLER_CONTRACTS: list[type] = [
    HandlerContract,
    InputReceivedHandlerContract,
    RouteMatchedHandlerContract,
    RouteNotMatchedHandlerContract,
    RouteDispatchedHandlerContract,
    ThrowableCaughtHandlerContract,
    ProcessExitingHandlerContract,
]


@pytest.mark.parametrize("contract", MIDDLEWARE_CONTRACTS + HANDLER_CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", MIDDLEWARE_CONTRACTS + HANDLER_CONTRACTS)
def test_the_contract_declares_an_abstract_method(contract: type) -> None:
    assert inspect.isabstract(contract)


@pytest.mark.parametrize("contract", HANDLER_CONTRACTS)
def test_every_handler_extends_the_handler_contract(contract: type) -> None:
    assert issubclass(contract, HandlerContract)


def test_every_handler_declares_add() -> None:
    for contract in HANDLER_CONTRACTS:
        assert hasattr(contract, "add")


@pytest.mark.parametrize(
    ("key", "value"),
    [
        (
            CliMiddlewareServiceId.INPUT_RECEIVED_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.InputReceivedHandlerContract",
        ),
        (
            CliMiddlewareServiceId.ROUTE_MATCHED_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.RouteMatchedHandlerContract",
        ),
        (
            CliMiddlewareServiceId.ROUTE_NOT_MATCHED_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.RouteNotMatchedHandlerContract",
        ),
        (
            CliMiddlewareServiceId.ROUTE_DISPATCHED_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.RouteDispatchedHandlerContract",
        ),
        (
            CliMiddlewareServiceId.THROWABLE_CAUGHT_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.ThrowableCaughtHandlerContract",
        ),
        (
            CliMiddlewareServiceId.PROCESS_EXITING_HANDLER_CONTRACT,
            "Valkyrja.Cli.Middleware.Handler.ProcessExitingHandlerContract",
        ),
    ],
)
def test_each_service_id(key: str, value: str) -> None:
    """Each key is part of the public API, so each test pins the whole string."""
    assert key == value
