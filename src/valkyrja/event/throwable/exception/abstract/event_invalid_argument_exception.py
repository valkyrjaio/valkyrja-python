#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.event.throwable.contract.event_throwable import EventThrowable
from valkyrja.throwable.exception.abstract.valkyrja_invalid_argument_exception import (
    ValkyrjaInvalidArgumentException,
)


class EventInvalidArgumentException(ValkyrjaInvalidArgumentException, EventThrowable):
    """The base invalid argument exception of the Event component."""

    _valkyrja_abstract = True
