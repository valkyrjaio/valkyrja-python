#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import ValkyrjaRuntimeException


class CliRuntimeException(ValkyrjaRuntimeException, CliThrowable):
    """The base runtime exception of the Cli component."""

    _valkyrja_abstract = True
