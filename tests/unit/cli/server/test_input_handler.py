#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Cli Server input handler and the exiter."""

from collections.abc import Iterator
from typing import Any

import pytest

from tests.fixtures.cli.middleware.short_circuit_input_middleware_fixture import (
    SHORT_CIRCUIT_INPUT_MIDDLEWARE_ID,
    ShortCircuitInputMiddlewareFixture,
)
from tests.fixtures.cli.routing.route_fixture import make_route
from valkyrja.cli.interaction.constant.cli_interaction_service_id import (
    CliInteractionServiceId,
)
from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.factory.output_factory import OutputFactory
from valkyrja.cli.middleware.handler.input_received_handler import InputReceivedHandler
from valkyrja.cli.middleware.handler.process_exiting_handler import ProcessExitingHandler
from valkyrja.cli.middleware.handler.route_dispatched_handler import RouteDispatchedHandler
from valkyrja.cli.middleware.handler.route_matched_handler import RouteMatchedHandler
from valkyrja.cli.middleware.handler.route_not_matched_handler import RouteNotMatchedHandler
from valkyrja.cli.middleware.handler.throwable_caught_handler import ThrowableCaughtHandler
from valkyrja.cli.routing.collection.route_collection import RouteCollection
from valkyrja.cli.routing.dispatcher.router import Router
from valkyrja.cli.server.constant.cli_server_service_id import CliServerServiceId
from valkyrja.cli.server.handler.input_handler import InputHandler
from valkyrja.cli.server.support.exiter import Exiter
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract


@pytest.fixture(autouse=True)
def frozen_exiter() -> Iterator[None]:
    Exiter.freeze()

    yield

    Exiter.unfreeze()


def make_handler(collection: RouteCollection, container: Container | None = None) -> InputHandler:
    container = container if container is not None else Container()
    router = Router(
        container=container,
        collection=collection,
        output_factory=OutputFactory(),
        throwable_caught_handler=ThrowableCaughtHandler(container),
        route_matched_handler=RouteMatchedHandler(container),
        route_not_matched_handler=RouteNotMatchedHandler(container),
        route_dispatched_handler=RouteDispatchedHandler(container),
        process_exiting_handler=ProcessExitingHandler(container),
    )

    return InputHandler(
        container=container,
        router=router,
        input_received_handler=InputReceivedHandler(container),
        throwable_caught_handler=ThrowableCaughtHandler(container),
        process_exiting_handler=ProcessExitingHandler(container),
        output_factory=OutputFactory(),
    )


def test_handle_answers_a_matched_command() -> None:
    handler = make_handler(RouteCollection().add(make_route("run")))

    output = handler.handle(Input(command_name="run"))

    assert isinstance(output, EmptyOutput)


def test_handle_publishes_the_input_and_the_output() -> None:
    container = Container()
    handler = make_handler(RouteCollection().add(make_route("run")), container)

    handler.handle(Input(command_name="run"))

    assert container.has(CliInteractionServiceId.INPUT_CONTRACT)
    assert container.has(CliInteractionServiceId.OUTPUT_CONTRACT)


def test_handle_answers_a_command_that_no_route_matches() -> None:
    handler = make_handler(RouteCollection())

    output = handler.handle(Input(command_name="missing"))

    assert output.get_exit_code() is ExitCode.ERROR


def test_handle_catches_a_throwable_from_the_command() -> None:
    def raising(container: ContainerContract, arguments: dict[str, Any]) -> OutputContract:
        raise RuntimeError("the command failed")

    handler = make_handler(RouteCollection().add(make_route("run").with_handler(raising)))

    output = handler.handle(Input(command_name="run"))

    assert output.get_exit_code() is ExitCode.ERROR
    assert "the command failed" in "".join(m.get_text() for m in output.get_messages())
    assert "run" in "".join(m.get_text() for m in output.get_messages())


def test_run_exits_with_the_code_of_the_output(monkeypatch: pytest.MonkeyPatch) -> None:
    """The frozen exiter makes `exit` a no-op, so the test records the code."""
    codes: list[int] = []
    monkeypatch.setattr(Exiter, "exit", staticmethod(codes.append))
    handler = make_handler(RouteCollection().add(make_route("run")))

    handler.run(Input(command_name="run"))

    assert codes == [ExitCode.SUCCESS.value]


def test_run_reads_an_integer_exit_code(monkeypatch: pytest.MonkeyPatch) -> None:
    codes: list[int] = []
    monkeypatch.setattr(Exiter, "exit", staticmethod(codes.append))

    def failing(container: ContainerContract, arguments: dict[str, Any]) -> OutputContract:
        return EmptyOutput(exit_code=7)

    handler = make_handler(RouteCollection().add(make_route("run").with_handler(failing)))

    handler.run(Input(command_name="run"))

    assert codes == [7]


def test_exit_runs_the_process_exiting_middleware() -> None:
    handler = make_handler(RouteCollection().add(make_route("run")))

    handler.exit(Input(command_name="run"), EmptyOutput())


def test_the_exiter_ends_the_process_when_it_is_not_frozen() -> None:
    Exiter.unfreeze()

    assert not Exiter.is_frozen()

    with pytest.raises(SystemExit) as exit_info:
        Exiter.exit(3)

    assert exit_info.value.code == 3


def test_the_service_ids() -> None:
    assert CliServerServiceId.INPUT_HANDLER_CONTRACT == "Valkyrja.Cli.Server.Handler.InputHandlerContract"


def test_an_input_received_middleware_can_answer_before_the_router() -> None:
    container = Container()
    container.bind(SHORT_CIRCUIT_INPUT_MIDDLEWARE_ID, lambda c, a: ShortCircuitInputMiddlewareFixture())
    handler = make_handler(RouteCollection().add(make_route("run")), container)
    handler._input_received_handler.add(SHORT_CIRCUIT_INPUT_MIDDLEWARE_ID)

    output = handler.handle(Input(command_name="run"))

    assert output.get_exit_code() is ExitCode.NO_INPUT


def test_a_frozen_exiter_does_not_end_the_process() -> None:
    """The autouse fixture freezes the exiter, so the call returns."""
    assert Exiter.is_frozen()
    assert Exiter.exit(1) is None
