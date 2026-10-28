#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Cli Server commands and the typo middleware."""

from typing import Any

from tests.fixtures.cli.routing.route_fixture import make_route
from valkyrja.cli.interaction.argument.argument import Argument
from valkyrja.cli.interaction.constant.cli_interaction_service_id import (
    CliInteractionServiceId,
)
from valkyrja.cli.interaction.input.input import Input
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.factory.output_factory import OutputFactory
from valkyrja.cli.middleware.handler.process_exiting_handler import ProcessExitingHandler
from valkyrja.cli.middleware.handler.route_dispatched_handler import RouteDispatchedHandler
from valkyrja.cli.middleware.handler.route_matched_handler import RouteMatchedHandler
from valkyrja.cli.middleware.handler.route_not_matched_handler import RouteNotMatchedHandler
from valkyrja.cli.middleware.handler.throwable_caught_handler import ThrowableCaughtHandler
from valkyrja.cli.routing.collection.route_collection import RouteCollection
from valkyrja.cli.routing.collector.attribute_route_collector import AttributeRouteCollector
from valkyrja.cli.routing.constant.cli_routing_service_id import CliRoutingServiceId
from valkyrja.cli.routing.dispatcher.router import Router
from valkyrja.cli.server.command.list_bash_command import (
    ListBashCommand,
    get_list_bash_help_text,
)
from valkyrja.cli.server.constant.cli_server_service_id import CliServerServiceId
from valkyrja.cli.server.constant.command_name import CommandName
from valkyrja.cli.server.middleware.route_not_matched.check_command_for_typo_middleware import (
    CheckCommandForTypoMiddleware,
)
from valkyrja.container.manager.container import Container


def make_container(collection: RouteCollection) -> Container:
    container = Container()
    container.set_singleton(CliRoutingServiceId.ROUTE_COLLECTION_CONTRACT, collection)
    container.set_singleton(CliInteractionServiceId.OUTPUT_FACTORY_CONTRACT, OutputFactory())

    return container


def get_text(messages: Any) -> str:
    return "".join(message.get_text() for message in messages)


def make_bash_route(namespace: str = "") -> Any:
    """Build the route that the bash command answers, carrying one namespace."""
    route = AttributeRouteCollector().get_routes(ListBashCommand)[0]
    namespace_parameter = route.get_arguments()[1].with_arguments(Argument(namespace))

    return route.with_arguments(route.get_arguments()[0], namespace_parameter)


def test_the_bash_command_lists_every_command() -> None:
    collection = RouteCollection().add(make_route("run")).add(make_route("stop"))

    output = ListBashCommand.run(make_container(collection), make_bash_route())

    assert get_text(output.get_messages()) == "run stop"


def test_the_bash_command_filters_by_a_namespace() -> None:
    collection = RouteCollection().add(make_route("app:run")).add(make_route("app:stop")).add(make_route("other"))

    output = ListBashCommand.run(make_container(collection), make_bash_route("app"))

    assert get_text(output.get_messages()) == "app:run app:stop"


def test_the_bash_command_drops_the_namespace_the_shell_already_typed() -> None:
    collection = RouteCollection().add(make_route("app:run")).add(make_route("app:stop"))

    output = ListBashCommand.run(make_container(collection), make_bash_route("app:"))

    assert get_text(output.get_messages()) == "run stop"


def test_the_bash_command_takes_no_namespace_as_every_command() -> None:
    collection = RouteCollection().add(make_route("run"))

    output = ListBashCommand.run(make_container(collection), make_bash_route())

    assert get_text(output.get_messages()) == "run"


def test_the_bash_command_carries_its_help_text() -> None:
    assert "bash completion" in get_list_bash_help_text().get_text()


def test_the_bash_command_marks_its_route() -> None:
    routes = AttributeRouteCollector().get_routes(ListBashCommand)

    assert [route.get_name() for route in routes] == [CommandName.LIST_BASH]
    assert [argument.get_name() for argument in routes[0].get_arguments()] == ["applicationName", "namespace"]
    assert routes[0].get_help_text()().get_text() == get_list_bash_help_text().get_text()


def make_typo_middleware(collection: RouteCollection, container: Container) -> CheckCommandForTypoMiddleware:
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

    return CheckCommandForTypoMiddleware(router, collection)


def test_the_typo_middleware_leaves_a_name_that_is_close_to_nothing() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
    middleware = make_typo_middleware(collection, container)
    output = EmptyOutput()

    answered = middleware.route_not_matched(
        Input(command_name="completely-different"), output, RouteNotMatchedHandler(container)
    )

    assert answered is output


def test_the_typo_middleware_offers_a_name_that_is_close() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
    middleware = make_typo_middleware(collection, container)

    # A non-interactive output takes the default answer, so the question reads no stdin.
    answered = middleware.route_not_matched(
        Input(command_name="ru"), EmptyOutput(is_interactive=False), RouteNotMatchedHandler(container)
    )

    assert "Did you mean to run one of the following commands?" in get_text(answered.get_messages())


def test_the_typo_middleware_runs_the_command_the_user_names() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
    middleware = make_typo_middleware(collection, container)
    commands = list(collection.all().values())

    middleware._question_callback(EmptyOutput(), _make_answer("run"), commands)

    assert middleware._matched_route is not None
    assert middleware._matched_route.get_name() == "run"


def test_the_typo_middleware_runs_nothing_when_the_user_declines() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
    middleware = make_typo_middleware(collection, container)

    middleware._question_callback(EmptyOutput(), _make_answer("no"), list(collection.all().values()))

    assert middleware._matched_route is None


def test_the_typo_middleware_runs_nothing_for_a_name_it_does_not_hold() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
    middleware = make_typo_middleware(collection, container)

    middleware._question_callback(EmptyOutput(), _make_answer("other"), list(collection.all().values()))

    assert middleware._matched_route is None


def test_the_typo_middleware_has_a_binding_key() -> None:
    assert CliServerServiceId.CHECK_COMMAND_FOR_TYPO_MIDDLEWARE == (
        "valkyrja.cli.server.middleware.route_not_matched.CheckCommandForTypoMiddleware"
    )


def _make_answer(response: str) -> Any:
    from valkyrja.cli.interaction.message.answer import Answer

    return Answer(default_response="no", allowed_responses=["run"]).with_user_response(response)


def test_the_typo_middleware_dispatches_the_command_the_user_chose() -> None:
    collection = RouteCollection().add(make_route("run"))
    container = make_container(collection)
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
    # A non-interactive output takes the default answer, so the default names the command.
    middleware = CheckCommandForTypoMiddleware(router, collection, default_answer="run")

    answered = middleware.route_not_matched(
        Input(command_name="ru"), EmptyOutput(is_interactive=False), RouteNotMatchedHandler(container)
    )

    assert middleware._matched_route is not None
    assert answered is not None
