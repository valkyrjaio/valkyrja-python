#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC

from valkyrja.http.message.throwable.contract.http_message_throwable import HttpMessageThrowable


class HttpStreamThrowable(HttpMessageThrowable, ABC):
    _valkyrja_abstract = True
