#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.container.throwable.exception.abstract.container_runtime_exception import (
    ContainerRuntimeException,
)


class ContainerInvalidPublishCallbackException(ContainerRuntimeException):
    pass
