#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC

from valkyrja.http.throwable.contract.http_throwable import HttpThrowable


class HttpMessageThrowable(HttpThrowable, ABC):
    """The contract that every throwable the Http Message subcomponent raises implements."""

    _valkyrja_abstract = True
