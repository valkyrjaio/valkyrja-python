#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Self, override

from valkyrja.container.throwable.exception.abstract.container_invalid_argument_exception import (
    ContainerInvalidArgumentException,
)


class ContainerInvalidReferenceException(ContainerInvalidArgumentException):
    def __init__(self, id_: str) -> None:
        super().__init__(f"Service with `{id_}` not found")

        self._id = id_

    @override
    def __reduce__(self) -> tuple[type[Self], tuple[str]]:
        # `BaseException.__reduce__` replays `args`, and `args` holds the built
        # message, so a copy would build the message from the message itself.
        return type(self), (self._id,)
