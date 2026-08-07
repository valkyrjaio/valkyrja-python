#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC
from typing import Any, Self

from valkyrja.throwable.factory.throwable_factory import ThrowableFactory


class ValkyrjaThrowable(BaseException, ABC):
    # Warning: `ABC` alone does not stop an exception from constructing, because
    # `BaseException.__new__` replaces the `object.__new__` that reads `__abstractmethods__`.
    _valkyrja_abstract = True

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Construct the throwable, unless the class is abstract."""
        if cls.__dict__.get("_valkyrja_abstract", False):
            raise TypeError(f"Can't instantiate abstract throwable {cls.__name__}")

        return super().__new__(cls, *args, **kwargs)

    def get_trace_code(self) -> str:
        """Get a trace code unique to the throwable that is raised.

        The method is concrete, so every throwable gets a trace code without
        writing this body again. `self` still resolves to the class that raised,
        so the code names that class.
        """
        return ThrowableFactory.get_trace_code(self)
