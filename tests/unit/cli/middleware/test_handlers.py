#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the middleware handlers."""

from collections.abc import Iterator

import pytest

from tests.fixtures.cli.middleware.recording_middleware_fixture import (
    CALLS,
    PassThroughMiddlewareFixture,
)
from tests.fixtures.cli.routing.route_fixture import make_route
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.middleware.handler.input_received_handler import InputReceivedHandler
from valkyrja.cli.middleware.handler.process_exiting_handler import ProcessExitingHandler
from valkyrja.cli.middleware.handler.route_dispatched_handler import RouteDispatchedHandler
from valkyrja.cli.middleware.handler.route_matched_handler import RouteMatchedHandler
from valkyrja.cli.middleware.handler.route_not_matched_handler import RouteNotMatchedHandler
from valkyrja.cli.middleware.handler.throwable_caught_handler import ThrowableCaughtHandler
from valkyrja.container.manager.container import Container

FIRST = "Valkyrja.Tests.Middleware.First"
SECOND = "Valkyrja.Tests.Middleware.Second"


@pytest.fixture(autouse=True)
def clear_calls() -> Iterator[None]:
    CALLS.clear()

    yield

    CALLS.clear()


def make_container() -> Container:
    container = Container()
    container.bind(FIRST, lambda c, a: PassThroughMiddlewareFixture("first"))
    container.bind(SECOND, lambda c, a: PassThroughMiddlewareFixture("second"))

    return container


def test_the_base_handler_holds_each_middleware() -> None:
    """PHP marks the base `abstract`. Python cannot, because the base implements
    the one abstract method that the contract declares. A subclass is what a
    caller uses, and the base carries the chain state for it.
    """
    handler = InputReceivedHandler(Container(), FIRST)

    handler.add(SECOND)

    assert handler._middleware == [FIRST, SECOND]


def test_an_input_received_handler_with_no_middleware_returns_the_input() -> None:
    input_ = Input()

    assert InputReceivedHandler(Container()).input_received(input_) is input_
    assert CALLS == []


def test_an_input_received_handler_runs_each_middleware_in_order() -> None:
    handler = InputReceivedHandler(make_container(), FIRST, SECOND)
    input_ = Input()

    assert handler.input_received(input_) is input_
    assert CALLS == ["first", "second"]


def test_add_appends_and_never_dedupes() -> None:
    handler = InputReceivedHandler(make_container(), FIRST)

    handler.add(FIRST)

    handler.input_received(Input())

    assert CALLS == ["first", "first"]


def test_a_route_matched_handler_returns_the_route_without_middleware() -> None:
    route = make_route()

    assert RouteMatchedHandler(Container()).route_matched(Input(), route) is route


def test_a_route_matched_handler_runs_each_middleware() -> None:
    handler = RouteMatchedHandler(make_container(), FIRST, SECOND)
    route = make_route()

    assert handler.route_matched(Input(), route) is route
    assert CALLS == ["first", "second"]


def test_a_route_not_matched_handler_returns_the_output_without_middleware() -> None:
    output = EmptyOutput()

    assert RouteNotMatchedHandler(Container()).route_not_matched(Input(), output) is output


def test_a_route_not_matched_handler_runs_each_middleware() -> None:
    handler = RouteNotMatchedHandler(make_container(), FIRST)
    output = EmptyOutput()

    assert handler.route_not_matched(Input(), output) is output
    assert CALLS == ["first"]


def test_a_route_dispatched_handler_returns_the_output_without_middleware() -> None:
    output = EmptyOutput()

    assert RouteDispatchedHandler(Container()).route_dispatched(Input(), output, make_route()) is output


def test_a_route_dispatched_handler_runs_each_middleware() -> None:
    handler = RouteDispatchedHandler(make_container(), FIRST)
    output = EmptyOutput()

    assert handler.route_dispatched(Input(), output, make_route()) is output
    assert CALLS == ["first"]


def test_a_throwable_caught_handler_returns_the_output_without_middleware() -> None:
    output = EmptyOutput()
    throwable = RuntimeError("boom")

    assert ThrowableCaughtHandler(Container()).throwable_caught(Input(), output, throwable) is output


def test_a_throwable_caught_handler_runs_each_middleware() -> None:
    handler = ThrowableCaughtHandler(make_container(), FIRST)
    output = EmptyOutput()

    assert handler.throwable_caught(Input(), output, RuntimeError("boom")) is output
    assert CALLS == ["first"]


def test_a_process_exiting_handler_does_nothing_without_middleware() -> None:
    ProcessExitingHandler(Container()).process_exiting(Input(), EmptyOutput())

    assert CALLS == []


def test_a_process_exiting_handler_runs_each_middleware() -> None:
    handler = ProcessExitingHandler(make_container(), FIRST, SECOND)

    handler.process_exiting(Input(), EmptyOutput())

    assert CALLS == ["first", "second"]
