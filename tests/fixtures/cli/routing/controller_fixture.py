#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final

from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.routing.attribute.route import route
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.data.option.help_option_parameter import HelpOptionParameter

FIRST_MIDDLEWARE_ID = "tests.middleware.First"


@final
class ControllerFixture:
    """A controller that marks two of its functions as commands."""

    @staticmethod
    @route(name="first", description="The first command")
    def first(container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()

    @staticmethod
    @route(
        name="second",
        description="The second command",
        route_matched_middleware=[FIRST_MIDDLEWARE_ID],
        options=[HelpOptionParameter()],
    )
    def second(container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()

    @staticmethod
    def not_a_command(container: Any, route: RouteContract) -> OutputContract:
        """A function with no marker, so the collector skips it."""
        return EmptyOutput()


@final
class EmptyControllerFixture:
    """A controller that marks no function."""

    @staticmethod
    def helper() -> None:
        """A function with no marker."""


@final
class MisplacedDecoratorControllerFixture:
    """A controller whose decorator sits over the static method, not under it."""

    @route(name="misplaced", description="The decorator sits over the static method")
    @staticmethod
    def misplaced(container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()


@final
class InstanceMethodControllerFixture:
    """A controller that marks an instance method, which takes an instance too."""

    @route(name="instance", description="An instance method")
    def instance(self, container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()


class BaseControllerFixture:
    """A controller that a second controller extends."""

    @staticmethod
    @route(name="inherited", description="A command a base class declares")
    def inherited(container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()


@final
class ExtendingControllerFixture(BaseControllerFixture):
    """A controller that inherits a command and adds one of its own."""

    @staticmethod
    @route(name="own", description="A command this class declares")
    def own(container: Any, route: RouteContract) -> OutputContract:
        return EmptyOutput()
