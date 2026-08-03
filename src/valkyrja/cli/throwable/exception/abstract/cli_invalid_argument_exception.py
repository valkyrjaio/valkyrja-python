#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


class CliInvalidArgumentException(ValkyrjaInvalidArgumentException, CliThrowable):
    """The base invalid argument exception of the Cli component."""

    _valkyrja_abstract = True
