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
    """The contract that every throwable the framework raises implements.

    The contract adds a trace code to the language root. A trace code
    correlates a log entry to a failure point, and the log does not have to
    show the stack trace to a user.
    """

    # Warning: `ABC` alone does not stop the instantiation of an exception
    # class. Only `object.__new__` reads `__abstractmethods__`, and
    # `BaseException.__new__` replaces it, so an abstract exception with an
    # unimplemented abstract method still constructs.
    #
    # Each abstract class in this hierarchy sets this flag, and `__new__` below
    # reads the flag from the class itself, never from a parent. A concrete
    # subclass does not set the flag, so the subclass stays instantiable.
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
