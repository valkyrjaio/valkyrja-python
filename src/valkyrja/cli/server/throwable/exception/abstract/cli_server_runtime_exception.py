#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.server.throwable.contract.cli_server_throwable import CliServerThrowable
from valkyrja.cli.throwable.exception.abstract.cli_runtime_exception import (
    CliRuntimeException,
)


class CliServerRuntimeException(CliRuntimeException, CliServerThrowable):
    _valkyrja_abstract = True
