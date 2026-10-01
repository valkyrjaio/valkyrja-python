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
from tests.fixtures.cli.server.failing_fixture import (
    CodelessOutputFixture,
    NamelessInputFixture,
    UnwritableOutputFixture,
)
from tests.fixtures.cli.server.raising_middleware_fixture import (
    RAISING_PROCESS_EXITING_MIDDLEWARE_ID,
    RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID,
    RaisingProcessExitingMiddlewareFixture,
    RaisingThrowableCaughtMiddlewareFixture,
)
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
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
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
    def raising(container: ContainerContract, route: RouteContract) -> OutputContract:
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

    def failing(container: ContainerContract, route: RouteContract) -> OutputContract:
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
    assert CliServerServiceId.INPUT_HANDLER_CONTRACT == "valkyrja.cli.server.handler.InputHandlerContract"


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


def make_handler_with(
    collection: RouteCollection,
    container: Container,
    throwable_caught_handler: ThrowableCaughtHandler | None = None,
    process_exiting_handler: ProcessExitingHandler | None = None,
) -> InputHandler:
    """Build a handler whose recovery stages a test can make fail."""
    throwable_caught_handler = (
        throwable_caught_handler if throwable_caught_handler is not None else ThrowableCaughtHandler(container)
    )
    process_exiting_handler = (
        process_exiting_handler if process_exiting_handler is not None else ProcessExitingHandler(container)
    )
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
        throwable_caught_handler=throwable_caught_handler,
        process_exiting_handler=process_exiting_handler,
        output_factory=OutputFactory(),
    )


def make_raising_route(name: str) -> Any:
    """Build a command whose handler raises."""

    def handle(container: ContainerContract, route: RouteContract) -> OutputContract:
        raise RuntimeError("the command failed")

    return make_route(name).with_handler(handle)


def test_handle_reports_a_recovery_that_failed() -> None:
    container = Container()
    container.set_singleton(RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID, RaisingThrowableCaughtMiddlewareFixture())
    throwable_caught_handler = ThrowableCaughtHandler(container, RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID)
    handler = make_handler_with(RouteCollection().add(make_raising_route("run")), container, throwable_caught_handler)

    output = handler.handle(Input(command_name="run"))
    text = "".join(message.get_text() for message in output.get_messages())

    assert output.get_exit_code() is ExitCode.ERROR
    assert "the command failed" in text
    assert "Recovery message:" in text
    assert "the recovery stage failed" in text


def test_the_recovery_report_leaves_out_an_input_it_cannot_read() -> None:
    container = Container()
    container.set_singleton(RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID, RaisingThrowableCaughtMiddlewareFixture())
    throwable_caught_handler = ThrowableCaughtHandler(container, RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID)
    handler = make_handler_with(RouteCollection().add(make_raising_route("run")), container, throwable_caught_handler)

    # The first report reads the command name, so an input that raises there takes it.
    output = handler.handle(NamelessInputFixture(command_name="run"))
    text = "".join(message.get_text() for message in output.get_messages())

    assert "Cli Server Error:" in text
    assert "Command:" not in text
    assert "Recovery message:" in text


def test_run_reports_a_write_that_failed() -> None:
    container = Container()
    handler = make_handler_with(RouteCollection(), container)

    handler.run(Input(command_name="run"))

    published = container.get_singleton(CliInteractionServiceId.OUTPUT_CONTRACT)

    assert isinstance(published, OutputContract)


def test_run_recovers_from_a_write_that_failed() -> None:
    container = Container()
    route = make_route("run").with_handler(lambda c, a: UnwritableOutputFixture())
    handler = make_handler_with(RouteCollection().add(route), container)

    handler.run(Input(command_name="run"))

    published = container.get_singleton(CliInteractionServiceId.OUTPUT_CONTRACT)

    assert isinstance(published, OutputContract)
    assert published.has_written_message()


def test_run_recovers_when_the_write_recovery_also_failed() -> None:
    container = Container()
    container.set_singleton(RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID, RaisingThrowableCaughtMiddlewareFixture())
    throwable_caught_handler = ThrowableCaughtHandler(container, RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID)
    route = make_route("run").with_handler(lambda c, a: UnwritableOutputFixture())
    handler = make_handler_with(RouteCollection().add(route), container, throwable_caught_handler)

    handler.run(Input(command_name="run"))

    published = container.get_singleton(CliInteractionServiceId.OUTPUT_CONTRACT)

    assert isinstance(published, OutputContract)
    assert published.get_exit_code() is ExitCode.ERROR


def test_run_reports_an_exit_stage_that_failed() -> None:
    container = Container()
    container.set_singleton(RAISING_PROCESS_EXITING_MIDDLEWARE_ID, RaisingProcessExitingMiddlewareFixture())
    process_exiting_handler = ProcessExitingHandler(container, RAISING_PROCESS_EXITING_MIDDLEWARE_ID)
    handler = make_handler_with(
        RouteCollection().add(make_route("run")), container, process_exiting_handler=process_exiting_handler
    )

    # The exit stage failure must not stop the run, because the exiter still ends it.
    handler.run(Input(command_name="run"))


def test_run_reports_an_exit_stage_whose_report_also_failed() -> None:
    container = Container()
    container.set_singleton(RAISING_PROCESS_EXITING_MIDDLEWARE_ID, RaisingProcessExitingMiddlewareFixture())
    process_exiting_handler = ProcessExitingHandler(container, RAISING_PROCESS_EXITING_MIDDLEWARE_ID)
    handler = make_handler_with(
        RouteCollection().add(make_route("run")), container, process_exiting_handler=process_exiting_handler
    )

    handler.run(NamelessInputFixture(command_name="run"))


def test_run_ends_with_an_error_when_the_exit_code_is_unreadable(monkeypatch: pytest.MonkeyPatch) -> None:
    codes: list[int] = []
    monkeypatch.setattr(Exiter, "exit", staticmethod(codes.append))
    container = Container()
    route = make_route("run").with_handler(lambda c, a: CodelessOutputFixture())
    handler = make_handler_with(RouteCollection().add(route), container)

    handler.run(Input(command_name="run"))

    assert codes == [ExitCode.ERROR.value]
