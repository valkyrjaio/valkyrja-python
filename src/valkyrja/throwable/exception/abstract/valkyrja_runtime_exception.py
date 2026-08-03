#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.throwable.contract.valkyrja_throwable import ValkyrjaThrowable
from valkyrja.throwable.factory.throwable_factory import ThrowableFactory


class ValkyrjaRuntimeException(ValkyrjaThrowable, RuntimeError):
    """The base runtime exception for every component.

    A component extends this class to get a `ComponentRuntimeException`, and a
    concrete exception extends that one.
    """

    # `ValkyrjaThrowable` comes first, because the method resolution order
    # decides which `__new__` runs. `RuntimeError` inherits a `__new__` that
    # constructs any class, so a base list that puts `RuntimeError` first
    # defeats the abstract guard on `ValkyrjaThrowable`.
    _valkyrja_abstract = True

    @override
    def get_trace_code(self) -> str:
        """Get a trace code unique to the throwable that is raised."""
        return ThrowableFactory.get_trace_code(self)
