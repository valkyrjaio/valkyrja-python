#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Route data object and the RouteCollection."""

import pytest

from tests.fixtures.cli.routing.route_fixture import ROUTE_NAME, handle, help_text, make_route
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.middleware.contract.route_matched_middleware_contract import (
    RouteMatchedMiddlewareContract,
)
from valkyrja.cli.routing.collection.route_collection import RouteCollection
from valkyrja.cli.routing.data.argument_parameter import ArgumentParameter
from valkyrja.cli.routing.data.cli_routing_data import CliRoutingData
from valkyrja.cli.routing.data.option_parameter import OptionParameter
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_argument_name_exception import (
    CliRoutingInvalidArgumentNameException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_option_name_exception import (
    CliRoutingInvalidOptionNameException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_route_name_exception import (
    CliRoutingInvalidRouteNameException,
)
from valkyrja.cli.routing.throwable.exception.cli_routing_no_help_text_exception import (
    CliRoutingNoHelpTextException,
)
from valkyrja.container.manager.container import Container


def test_a_route_holds_its_name_and_description() -> None:
    route = make_route()

    assert route.get_name() == ROUTE_NAME
    assert route.get_description() == "A command that a test runs"
    assert route.get_handler() is handle


def test_the_route_setters_return_copies() -> None:
    route = make_route()

    assert route.with_name("other").get_name() == "other"
    assert route.with_description("Other").get_description() == "Other"
    assert route.with_handler(handle).get_handler() is handle
    assert route.get_name() == ROUTE_NAME


def test_a_route_without_help_text_raises_when_asked_for_it() -> None:
    with pytest.raises(CliRoutingNoHelpTextException, match="No help text exists"):
        make_route().get_help_text()


def test_a_route_builds_its_help_text_only_when_asked() -> None:
    route = make_route().with_help_text(help_text)

    assert route.has_help_text()
    assert route.get_help_text_message().get_text() == "The help text"


def test_a_route_holds_arguments() -> None:
    route = make_route().with_arguments(ArgumentParameter("first"))

    assert route.has_arguments()
    assert route.has_argument("first")
    assert route.get_argument("first").get_name() == "first"
    assert not route.has_argument("missing")

    added = route.with_added_arguments(ArgumentParameter("second"))

    assert len(added.get_arguments()) == 2
    assert len(route.get_arguments()) == 1


def test_a_route_without_arguments() -> None:
    route = make_route()

    assert not route.has_arguments()
    assert route.get_arguments() == []

    with pytest.raises(CliRoutingInvalidArgumentNameException, match="was not found"):
        route.get_argument("missing")


def test_a_route_holds_options() -> None:
    route = make_route().with_options(OptionParameter("help", short_names=["h"]))

    assert route.has_options()
    assert route.has_option("help")
    assert route.has_option("h")
    assert route.get_option("h").get_name() == "help"

    added = route.with_added_options(OptionParameter("quiet"))

    assert len(added.get_options()) == 2
    assert len(route.get_options()) == 1


def test_a_route_without_options() -> None:
    route = make_route()

    assert not route.has_options()

    with pytest.raises(CliRoutingInvalidOptionNameException, match="was not found"):
        route.get_option("missing")


@pytest.mark.parametrize("family", ["route_matched", "route_dispatched", "throwable_caught", "process_exiting"])
def test_each_middleware_family_appends_and_never_dedupes(family: str) -> None:
    route = make_route()
    get = getattr(route, f"get_{family}_middleware")
    with_ = getattr(route, f"with_{family}_middleware")

    assert get() == []

    scheduled = with_(RouteMatchedMiddlewareContract)

    assert getattr(scheduled, f"get_{family}_middleware")() == [RouteMatchedMiddlewareContract]

    twice = getattr(scheduled, f"with_added_{family}_middleware")(RouteMatchedMiddlewareContract)

    assert getattr(twice, f"get_{family}_middleware")() == [
        RouteMatchedMiddlewareContract,
        RouteMatchedMiddlewareContract,
    ]
    assert get() == []


def test_get_arguments_and_options_copy_their_lists() -> None:
    route = make_route().with_arguments(ArgumentParameter("a")).with_options(OptionParameter("o"))

    route.get_arguments().clear()
    route.get_options().clear()

    assert len(route.get_arguments()) == 1
    assert len(route.get_options()) == 1


def test_a_new_collection_is_empty() -> None:
    collection = RouteCollection()

    assert collection.all() == {}
    assert not collection.has(ROUTE_NAME)


def test_add_registers_a_route_by_name() -> None:
    collection = RouteCollection()
    route = make_route()

    assert collection.add(route) is collection
    assert collection.has(ROUTE_NAME)
    assert collection.get(ROUTE_NAME) is route
    assert list(collection.all()) == [ROUTE_NAME]


def test_get_raises_for_an_unknown_name() -> None:
    with pytest.raises(CliRoutingInvalidRouteNameException, match="was not found"):
        RouteCollection().get("missing")


def test_get_data_returns_the_state() -> None:
    collection = RouteCollection().add(make_route())

    data = collection.get_data()

    assert list(data.routes) == [ROUTE_NAME]
    assert data.routes[ROUTE_NAME]().get_name() == ROUTE_NAME


def test_get_data_copies_the_state() -> None:
    collection = RouteCollection().add(make_route())

    collection.get_data().routes.clear()

    assert collection.has(ROUTE_NAME)


def test_set_from_data_replaces_the_state() -> None:
    collection = RouteCollection().add(make_route("first"))
    route = make_route("cached")

    collection.set_from_data(CliRoutingData(routes={"cached": lambda: route}))

    assert not collection.has("first")
    assert collection.get("cached") is route


def test_the_data_defaults_to_no_route() -> None:
    assert CliRoutingData().routes == {}


def test_a_route_handler_answers_with_an_output() -> None:
    output = make_route().get_handler()(Container(), {})

    assert isinstance(output, EmptyOutput)
