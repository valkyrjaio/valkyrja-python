#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.server.throwable.contract.cli_server_throwable import CliServerThrowable
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


class CliServerInvalidArgumentException(ValkyrjaInvalidArgumentException, CliServerThrowable):
    """The base invalid argument exception of the Cli Server subcomponent."""

    _valkyrja_abstract = True
