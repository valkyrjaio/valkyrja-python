#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.event.throwable.contract.event_throwable import EventThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import ValkyrjaRuntimeException


class EventRuntimeException(ValkyrjaRuntimeException, EventThrowable):
    """The base runtime exception of the Event component."""

    _valkyrja_abstract = True
