#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.routing.throwable.contract.cli_routing_throwable import (
    CliRoutingThrowable,
)
from valkyrja.cli.throwable.exception.abstract.cli_invalid_argument_exception import (
    CliInvalidArgumentException,
)


class CliRoutingInvalidArgumentException(CliInvalidArgumentException, CliRoutingThrowable):
    _valkyrja_abstract = True
