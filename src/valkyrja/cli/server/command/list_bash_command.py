#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import cast

from valkyrja.cli.interaction.constant.cli_interaction_service_id import (
    CliInteractionServiceId,
)
from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.interaction.output.factory.contract.output_factory_contract import (
    OutputFactoryContract,
)
from valkyrja.cli.routing.attribute.route import route
from valkyrja.cli.routing.collection.contract.route_collection_contract import (
    RouteCollectionContract,
)
from valkyrja.cli.routing.constant.cli_routing_service_id import CliRoutingServiceId
from valkyrja.cli.routing.data.argument_parameter import ArgumentParameter
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.server.constant.command_name import CommandName
from valkyrja.container.manager.contract.container_contract import ContainerContract


def get_list_bash_help_text() -> MessageContract:
    """Get the help text of the bash completion command."""
    return Message("A command to list all the commands present within the Cli component for bash completion.")


class ListBashCommand:
    @staticmethod
    @route(
        name=CommandName.LIST_BASH,
        description="List all commands for bash completion",
        help_text=get_list_bash_help_text,
        arguments=[
            ArgumentParameter(name="applicationName", description="The application name"),
            ArgumentParameter(name="namespace", description="An optional namespace to filter commands by"),
        ],
    )
    def run(container: ContainerContract, route: RouteContract) -> OutputContract:
        """Write each command name on one line, so bash completes one of them."""
        collection = cast("RouteCollectionContract", container.get(CliRoutingServiceId.ROUTE_COLLECTION_CONTRACT))
        output_factory = cast("OutputFactoryContract", container.get(CliInteractionServiceId.OUTPUT_FACTORY_CONTRACT))
        namespace = route.get_argument_value("namespace")
        names = list(collection.all())

        if namespace != "":
            names = [name for name in names if name.startswith(namespace)]
            colon_at = namespace.find(":")

            # A namespaced command completes on the part after the colon, because bash
            # already holds the namespace it typed.
            if colon_at != -1:
                names = [name[colon_at + 1 :] for name in names]

        return output_factory.create_output().with_added_message(Message(" ".join(names)))
