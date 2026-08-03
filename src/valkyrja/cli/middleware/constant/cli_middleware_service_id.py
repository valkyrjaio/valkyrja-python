#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class CliMiddlewareServiceId:
    """The binding key for each service of the Cli Middleware subcomponent."""

    INPUT_RECEIVED_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.InputReceivedHandlerContract"
    ROUTE_MATCHED_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.RouteMatchedHandlerContract"
    ROUTE_NOT_MATCHED_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.RouteNotMatchedHandlerContract"
    ROUTE_DISPATCHED_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.RouteDispatchedHandlerContract"
    THROWABLE_CAUGHT_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.ThrowableCaughtHandlerContract"
    PROCESS_EXITING_HANDLER_CONTRACT: Final[str] = "Valkyrja.Cli.Middleware.Handler.ProcessExitingHandlerContract"
