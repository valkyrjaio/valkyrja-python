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
from valkyrja.cli.routing.data.option.help_option_parameter import HelpOptionParameter

FIRST_MIDDLEWARE_ID = "Valkyrja.Tests.Middleware.First"


@final
class ControllerFixture:
    """A controller that marks two of its functions as commands."""

    @staticmethod
    @route(name="first", description="The first command")
    def first(container: Any, arguments: dict[str, Any]) -> OutputContract:
        return EmptyOutput()

    @staticmethod
    @route(
        name="second",
        description="The second command",
        route_matched_middleware=[FIRST_MIDDLEWARE_ID],
        options=[HelpOptionParameter()],
    )
    def second(container: Any, arguments: dict[str, Any]) -> OutputContract:
        return EmptyOutput()

    @staticmethod
    def not_a_command(container: Any, arguments: dict[str, Any]) -> OutputContract:
        """A function with no marker, so the collector skips it."""
        return EmptyOutput()


@final
class EmptyControllerFixture:
    """A controller that marks no function."""

    @staticmethod
    def helper() -> None:
        """A function with no marker."""
