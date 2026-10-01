#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the AttributeRouteCollector and the `@route` decorator."""

import pytest

from tests.fixtures.cli.routing.controller_fixture import (
    FIRST_MIDDLEWARE_ID,
    ControllerFixture,
    EmptyControllerFixture,
    ExtendingControllerFixture,
    InstanceMethodControllerFixture,
    MisplacedDecoratorControllerFixture,
)
from tests.fixtures.cli.routing.route_fixture import make_route
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.routing.attribute.route import ROUTE_MARKER, RouteMarker
from valkyrja.cli.routing.collector.attribute_route_collector import AttributeRouteCollector
from valkyrja.cli.routing.throwable.exception.cli_routing_invalid_route_handler_exception import (
    CliRoutingInvalidRouteHandlerException,
)
from valkyrja.container.manager.container import Container


def test_the_decorator_attaches_a_marker_and_returns_the_function() -> None:
    marker = getattr(ControllerFixture.first, ROUTE_MARKER)

    assert isinstance(marker, RouteMarker)
    assert marker.name == "first"
    assert marker.description == "The first command"


def test_the_decorator_registers_nothing() -> None:
    """The marker is metadata alone, so the function still answers a call."""
    assert isinstance(ControllerFixture.first(Container(), make_route()), EmptyOutput)


def test_the_collector_reads_each_marked_function() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture)

    assert sorted(route.get_name() for route in routes) == ["first", "second"]


def test_the_collector_skips_a_function_with_no_marker() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture)

    assert "not_a_command" not in [route.get_name() for route in routes]


def test_the_collector_reads_no_route_from_an_unmarked_class() -> None:
    assert AttributeRouteCollector().get_routes(EmptyControllerFixture) == []


def test_the_collector_reads_several_classes() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture, EmptyControllerFixture)

    assert len(routes) == 2


def test_the_collector_carries_the_middleware_and_the_options() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture)
    second = next(route for route in routes if route.get_name() == "second")

    assert second.get_route_matched_middleware() == [FIRST_MIDDLEWARE_ID]
    assert second.has_option("help")


def test_the_route_handler_is_the_marked_function() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture)
    first = next(route for route in routes if route.get_name() == "first")

    assert isinstance(first.get_handler()(Container(), make_route()), EmptyOutput)


def test_a_route_with_no_middleware_starts_empty() -> None:
    routes = AttributeRouteCollector().get_routes(ControllerFixture)
    first = next(route for route in routes if route.get_name() == "first")

    assert first.get_route_matched_middleware() == []
    assert not first.has_options()
    assert not first.has_help_text()


def test_the_collector_reads_a_decorator_that_sits_over_the_static_method() -> None:
    routes = AttributeRouteCollector().get_routes(MisplacedDecoratorControllerFixture)

    assert [route.get_name() for route in routes] == ["misplaced"]


def test_the_collector_reports_a_marked_instance_method() -> None:
    # A handler takes the container and the arguments alone, so an instance method
    # would read the container as its instance.
    with pytest.raises(CliRoutingInvalidRouteHandlerException, match="is no static method"):
        AttributeRouteCollector().get_routes(InstanceMethodControllerFixture)


def test_the_collector_reads_a_command_that_a_base_class_declares() -> None:
    routes = AttributeRouteCollector().get_routes(ExtendingControllerFixture)

    assert sorted(route.get_name() for route in routes) == ["inherited", "own"]
