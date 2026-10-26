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


class ContainerCyclicAliasException(ContainerInvalidArgumentException):
    def __init__(self, alias: str, id_: str) -> None:
        message = (
            f"Alias `{alias}` cannot point at itself."
            if alias == id_
            else f"Alias `{alias}` cannot reach `{id_}`, because the chain from `{id_}` returns to `{alias}`."
        )

        super().__init__(message)

        self._alias = alias
        self._id = id_

    @override
    def __reduce__(self) -> tuple[type[Self], tuple[str, str]]:
        # `BaseException.__reduce__` replays `args`, and `args` holds the built
        # message, so a copy would build the message from the message itself.
        return type(self), (self._alias, self._id)
