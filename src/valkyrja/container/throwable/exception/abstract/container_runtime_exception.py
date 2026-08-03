#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from valkyrja.container.throwable.contract.container_throwable import ContainerThrowable
from valkyrja.throwable.exception.abstract.valkyrja_runtime_exception import ValkyrjaRuntimeException


class ContainerRuntimeException(ValkyrjaRuntimeException, ContainerThrowable):
    """The base runtime exception of the Container component."""

    _valkyrja_abstract = True
