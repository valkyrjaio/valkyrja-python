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
from valkyrja.cli.middleware.contract.process_exiting_middleware_contract import (
    ProcessExitingMiddlewareContract,
)
from valkyrja.cli.middleware.contract.throwable_caught_middleware_contract import (
    ThrowableCaughtMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.process_exiting_handler_contract import (
    ProcessExitingHandlerContract,
)
from valkyrja.cli.middleware.handler.contract.throwable_caught_handler_contract import (
    ThrowableCaughtHandlerContract,
)

RAISING_THROWABLE_CAUGHT_MIDDLEWARE_ID = "tests.fixtures.cli.server.RaisingThrowableCaughtMiddlewareFixture"
RAISING_PROCESS_EXITING_MIDDLEWARE_ID = "tests.fixtures.cli.server.RaisingProcessExitingMiddlewareFixture"


@final
class RaisingThrowableCaughtMiddlewareFixture(ThrowableCaughtMiddlewareContract):
    """A middleware that fails while the handler reports another failure."""

    @override
    def throwable_caught(
        self,
        input_: InputContract,
        output: OutputContract,
        throwable: BaseException,
        handler: ThrowableCaughtHandlerContract,
    ) -> OutputContract:
        raise RuntimeError("the recovery stage failed")


@final
class RaisingProcessExitingMiddlewareFixture(ProcessExitingMiddlewareContract):
    """A middleware that fails while the process exits."""

    @override
    def process_exiting(
        self,
        input_: InputContract,
        output: OutputContract,
        handler: ProcessExitingHandlerContract,
    ) -> None:
        raise RuntimeError("the exit stage failed")
