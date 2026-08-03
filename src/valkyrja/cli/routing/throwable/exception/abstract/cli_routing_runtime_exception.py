#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.routing.throwable.contract.cli_routing_throwable import CliRoutingThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import (
    ValkyrjaRuntimeException,
)


class CliRoutingRuntimeException(ValkyrjaRuntimeException, CliRoutingThrowable):
    """The base runtime exception of the Cli Routing subcomponent."""

    _valkyrja_abstract = True
