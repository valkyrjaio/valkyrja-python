#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.event.throwable.exception.abstract.event_invalid_argument_exception import (
    EventInvalidArgumentException,
)


class EventInvalidEventException(EventInvalidArgumentException):
    def __init__(self, id_: str) -> None:
        super().__init__(f"Service with `{id_}` is not an event")

        self._id = id_

    def get_id(self) -> str:
        """Get the binding key that resolved to a thing that is not an event."""
        return self._id
