#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.routing.throwable.exception.abstract.cli_routing_runtime_exception import (
    CliRoutingRuntimeException,
)


class CliRoutingNoHelpTextException(CliRoutingRuntimeException):
    """The route carries no help text, and a caller asked for it."""
