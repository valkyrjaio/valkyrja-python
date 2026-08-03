#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.routing.throwable.exception.abstract.cli_routing_invalid_argument_exception import (
    CliRoutingInvalidArgumentException,
)


class CliRoutingInvalidArgumentNameException(CliRoutingInvalidArgumentException):
    """The route declares no argument with that name."""
