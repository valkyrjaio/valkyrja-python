#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.routing.data.route import Route
from valkyrja.container.manager.contract.container_contract import ContainerContract

ROUTE_NAME = "tests:run"


def handle(container: ContainerContract, arguments: dict[str, Any]) -> OutputContract:
    """Answer the command with an empty output."""
    return EmptyOutput()


def help_text() -> MessageContract:
    """Build the help text only when a reader asks for it."""
    return Message("The help text")


def make_route(name: str = ROUTE_NAME) -> Route:
    """Build a route that a test drives."""
    return Route(name=name, description="A command that a test runs", handler=handle)
