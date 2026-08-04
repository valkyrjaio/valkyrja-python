#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.container.throwable.exception.abstract.container_invalid_argument_exception import (
    ContainerInvalidArgumentException,
)


class ContainerInvalidReferenceException(ContainerInvalidArgumentException):
    """The container has no service for a given id."""

    def __init__(self, id_: str) -> None:
        super().__init__(f"Service with `{id_}` not found")
