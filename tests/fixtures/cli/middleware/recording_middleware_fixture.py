#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.input_received_middleware_contract import (
    InputReceivedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.process_exiting_middleware_contract import (
    ProcessExitingMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_dispatched_middleware_contract import (
    RouteDispatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_matched_middleware_contract import (
    RouteMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.route_not_matched_middleware_contract import (
    RouteNotMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.input_received_handler_contract import (
    InputReceivedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_dispatched_handler_contract import (
    RouteDispatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_matched_handler_contract import (
    RouteMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)
from valkyrja.cli.routing.data.contract.route_contract import RouteContract

CALLS: list[str] = []
"""Each middleware records its name here, so a test reads the order."""


@final
class PassThroughMiddlewareFixture(
    InputReceivedMiddlewareContract,
    RouteMatchedMiddlewareContract,
    RouteNotMatchedMiddlewareContract,
    RouteDispatchedMiddlewareContract,
    ThrowableCaughtMiddlewareContract,
    ProcessExitingMiddlewareContract,
):
    """A middleware that records the call and gives the chain onward."""

    def __init__(self, name: str = "pass") -> None:
        self.name = name

    @override
    def input_received(
        self, input_: InputContract, handler: InputReceivedHandlerContract
    ) -> InputContract | OutputContract:
        CALLS.append(self.name)

        return handler.input_received(input_)

    @override
    def route_matched(
        self, input_: InputContract, route: RouteContract, handler: RouteMatchedHandlerContract
    ) -> RouteContract | OutputContract:
        CALLS.append(self.name)

        return handler.route_matched(input_, route)

    @override
    def route_not_matched(
        self,
        input_: InputContract,
        output: OutputContract,
        handler: RouteNotMatchedHandlerContract,
    ) -> OutputContract:
        CALLS.append(self.name)

        return handler.route_not_matched(input_, output)

    @override
    def route_dispatched(
        self,
        input_: InputContract,
        output: OutputContract,
        route: RouteContract,
        handler: RouteDispatchedHandlerContract,
    ) -> OutputContract:
        CALLS.append(self.name)

        return handler.route_dispatched(input_, output, route)

    @override
    def throwable_caught(
        self,
        input_: InputContract,
        output: OutputContract,
        throwable: BaseException,
        handler: ThrowableCaughtHandlerContract,
    ) -> OutputContract:
        CALLS.append(self.name)

        return handler.throwable_caught(input_, output, throwable)

    @override
    def process_exiting(
        self, input_: InputContract, output: OutputContract, handler: ProcessExitingHandlerContract
    ) -> None:
        CALLS.append(self.name)

        handler.process_exiting(input_, output)
