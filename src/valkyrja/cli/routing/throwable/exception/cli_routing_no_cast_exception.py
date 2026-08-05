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


class CliRoutingNoCastException(CliRoutingRuntimeException):
    """A parameter has no cast, and a caller asked for one."""
