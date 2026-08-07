#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC

from valkyrja.cli.throwable.contract.cli_throwable import CliThrowable


class CliInteractionThrowable(CliThrowable, ABC):
    _valkyrja_abstract = True
