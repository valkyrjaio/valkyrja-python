#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Self, override

from valkyrja.container.throwable.exception.abstract.container_runtime_exception import (
    ContainerRuntimeException,
)


class ContainerUnresolvedParentAliasException(ContainerRuntimeException):
    def __init__(self, alias: str, reached_id: str) -> None:
        super().__init__(
            f"Alias `{alias}` reaches `{reached_id}`, which the parent container has not resolved. "
            "Resolve or publish it in bootstrap_parent_services() before the request loop begins."
        )

        self._alias = alias
        self._reached_id = reached_id

    @override
    def __reduce__(self) -> tuple[type[Self], tuple[str, str]]:
        # `BaseException.__reduce__` replays `args`, and `args` holds the built
        # message, so a copy would build the message from the message itself.
        return type(self), (self._alias, self._reached_id)
