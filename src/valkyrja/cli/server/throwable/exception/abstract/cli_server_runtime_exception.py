#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.server.throwable.contract.cli_server_throwable import CliServerThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import (
    ValkyrjaRuntimeException,
)


class CliServerRuntimeException(ValkyrjaRuntimeException, CliServerThrowable):
    """The base runtime exception of the Cli Server subcomponent."""

    _valkyrja_abstract = True
