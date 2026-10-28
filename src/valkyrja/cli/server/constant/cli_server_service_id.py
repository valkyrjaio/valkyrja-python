#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CliServerServiceId:
    INPUT_HANDLER_CONTRACT: Final[str] = "valkyrja.cli.server.handler.InputHandlerContract"
    CHECK_FOR_HELP_OPTIONS_MIDDLEWARE: Final[str] = (
        "valkyrja.cli.server.middleware.input_received.CheckForHelpOptionsMiddleware"
    )
    CHECK_FOR_VERSION_OPTIONS_MIDDLEWARE: Final[str] = (
        "valkyrja.cli.server.middleware.input_received.CheckForVersionOptionsMiddleware"
    )
    CHECK_GLOBAL_INTERACTION_OPTIONS_MIDDLEWARE: Final[str] = (
        "valkyrja.cli.server.middleware.input_received.CheckGlobalInteractionOptionsMiddleware"
    )
    OUTPUT_THROWABLE_CAUGHT_MIDDLEWARE: Final[str] = (
        "valkyrja.cli.server.middleware.throwable_caught.OutputThrowableCaughtMiddleware"
    )
    CHECK_COMMAND_FOR_TYPO_MIDDLEWARE: Final[str] = (
        "valkyrja.cli.server.middleware.route_not_matched.CheckCommandForTypoMiddleware"
    )
