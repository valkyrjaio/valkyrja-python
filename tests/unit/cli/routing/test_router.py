#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Cli Router."""

from typing import Any, cast

from tests.fixtures.cli.middleware.short_circuit_middleware_fixture import (
    SHORT_CIRCUIT_MIDDLEWARE_ID,
    ShortCircuitMiddlewareFixture,
)
from tests.fixtures.cli.routing.route_fixture import make_route
from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.option.option import Option
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.factory.output_factory import OutputFactory
from valkyrja.cli.middleware.handler.process_exiting_handler import ProcessExitingHandler
from valkyrja.cli.middleware.handler.route_dispatched_handler import RouteDispatchedHandler
from valkyrja.cli.middleware.handler.route_matched_handler import RouteMatchedHandler
from valkyrja.cli.middleware.handler.route_not_matched_handler import RouteNotMatchedHandler
from valkyrja.cli.middleware.handler.throwable_caught_handler import ThrowableCaughtHandler
from valkyrja.cli.routing.collection.route_collection import RouteCollection
from valkyrja.cli.routing.constant.cli_routing_service_id import CliRoutingServiceId
from valkyrja.cli.routing.data.argument_parameter import ArgumentParameter
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.data.option_parameter import OptionParameter
from valkyrja.cli.routing.dispatcher.router import Router
from valkyrja.cli.routing.enum.argument_mode import ArgumentMode
from valkyrja.cli.routing.enum.argument_value_mode import ArgumentValueMode
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract


def make_router(collection: RouteCollection, container: Container | None = None) -> Router:
    container = container if container is not None else Container()

    return Router(
        container=container,
        collection=collection,
        output_factory=OutputFactory(),
        throwable_caught_handler=ThrowableCaughtHandler(container),
        route_matched_handler=RouteMatchedHandler(container),
        route_not_matched_handler=RouteNotMatchedHandler(container),
        route_dispatched_handler=RouteDispatchedHandler(container),
        process_exiting_handler=ProcessExitingHandler(container),
    )


def test_dispatch_answers_a_command_that_no_route_matches() -> None:
    router = make_router(RouteCollection())

    output = router.dispatch(Input(command_name="missing"))

    assert output.get_exit_code() is ExitCode.ERROR
    assert "was not found" in output.get_messages()[0].get_text()


def test_dispatch_runs_the_handler_of_the_matched_route() -> None:
    seen: list[ContainerContract] = []

    def handle(container: ContainerContract, arguments: dict[str, Any]) -> OutputContract:
        seen.append(container)

        return EmptyOutput()

    container = Container()
    route = make_route("run").with_handler(handle)
    router = make_router(RouteCollection().add(route), container)

    output = router.dispatch(Input(command_name="run"))

    assert isinstance(output, EmptyOutput)
    assert seen == [container]


def test_dispatch_publishes_the_route_in_the_container() -> None:
    container = Container()
    route = make_route("run")
    router = make_router(RouteCollection().add(route), container)

    router.dispatch(Input(command_name="run"))

    assert cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT)).get_name() == "run"


def test_dispatch_route_fills_a_single_value_argument() -> None:
    container = Container()
    route = make_route("run").with_arguments(ArgumentParameter("first", mode=ArgumentMode.OPTIONAL))
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run", arguments=[Argument("a")]), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert [a.get_value() for a in filled.get_argument("first").get_arguments()] == ["a"]


def test_dispatch_route_gives_every_argument_to_an_array_parameter() -> None:
    container = Container()
    route = make_route("run").with_arguments(
        ArgumentParameter("many", mode=ArgumentMode.OPTIONAL, value_mode=ArgumentValueMode.ARRAY)
    )
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run", arguments=[Argument("a"), Argument("b")]), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert [a.get_value() for a in filled.get_argument("many").get_arguments()] == ["a", "b"]


def test_dispatch_route_gives_an_array_parameter_only_what_is_left() -> None:
    container = Container()
    route = make_route("run").with_arguments(
        ArgumentParameter("first", mode=ArgumentMode.OPTIONAL),
        ArgumentParameter("rest", mode=ArgumentMode.OPTIONAL, value_mode=ArgumentValueMode.ARRAY),
    )
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run", arguments=[Argument("a"), Argument("b"), Argument("c")]), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert [a.get_value() for a in filled.get_argument("first").get_arguments()] == ["a"]
    assert [a.get_value() for a in filled.get_argument("rest").get_arguments()] == ["b", "c"]


def test_dispatch_route_fills_every_positional_argument_in_order() -> None:
    container = Container()
    route = make_route("run").with_arguments(
        ArgumentParameter("first", mode=ArgumentMode.OPTIONAL),
        ArgumentParameter("second", mode=ArgumentMode.OPTIONAL),
    )
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run", arguments=[Argument("a"), Argument("b")]), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert filled.get_argument("first").get_first_value() == "a"
    assert filled.get_argument("second").get_first_value() == "b"


def test_dispatch_route_leaves_an_argument_with_no_input_empty() -> None:
    container = Container()
    route = make_route("run").with_arguments(ArgumentParameter("first", mode=ArgumentMode.OPTIONAL))
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run"), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert filled.get_argument("first").get_arguments() == []


def test_dispatch_route_fills_an_option_by_name_and_by_short_name() -> None:
    container = Container()
    route = make_route("run").with_options(OptionParameter("verbose", short_names=["v"]))
    router = make_router(RouteCollection().add(route), container)

    router.dispatch_route(Input(command_name="run", options=[Option("v"), Option("other")]), route)

    filled = cast("RouteContract", container.get_singleton(CliRoutingServiceId.ROUTE_CONTRACT))

    assert len(filled.get_option("verbose").get_options()) == 1


def test_the_service_ids() -> None:
    assert CliRoutingServiceId.ROUTE_CONTRACT == "Valkyrja.Cli.Routing.Data.RouteContract"
    assert CliRoutingServiceId.ROUTER_CONTRACT == "Valkyrja.Cli.Routing.Dispatcher.RouterContract"
    assert CliRoutingServiceId.ROUTE_COLLECTION_CONTRACT == "Valkyrja.Cli.Routing.Collection.RouteCollectionContract"
    assert CliRoutingServiceId.CLI_ROUTING_DATA == "Valkyrja.Cli.Routing.Data.CliRoutingData"


def test_a_route_matched_middleware_can_answer_with_an_output() -> None:
    container = Container()
    container.bind(SHORT_CIRCUIT_MIDDLEWARE_ID, lambda c, a: ShortCircuitMiddlewareFixture())
    route = make_route("run").with_route_matched_middleware(SHORT_CIRCUIT_MIDDLEWARE_ID)
    router = make_router(RouteCollection().add(route), container)

    output = router.dispatch(Input(command_name="run"))

    assert output.get_exit_code() is ExitCode.USAGE_ERROR
