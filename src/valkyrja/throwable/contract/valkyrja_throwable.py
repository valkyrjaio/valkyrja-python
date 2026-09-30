#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC
from itertools import islice
from traceback import walk_stack
from typing import Any, Self

from valkyrja.throwable.factory.throwable_factory import ConstructionFrame, ThrowableFactory


class ValkyrjaThrowable(BaseException, ABC):
    # Warning: `ABC` alone does not stop an exception from constructing, because
    # `BaseException.__new__` replaces the `object.__new__` that reads `__abstractmethods__`.
    _valkyrja_abstract = True

    _construction_stack: tuple[ConstructionFrame, ...]

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        """Construct the throwable, unless the class is abstract."""
        if cls.__dict__.get("_valkyrja_abstract", False):
            raise TypeError(f"Can't instantiate abstract throwable {cls.__name__}")

        throwable = super().__new__(cls, *args, **kwargs)
        # The stack is read here, at the construction site, because `__traceback__`
        # is empty until the raise and grows with every frame the raise passes.
        # `walk_stack` opens on this frame, so the first entry is dropped. Each
        # frame becomes a tuple of plain values, so the throwable stays picklable.
        throwable._construction_stack = tuple(
            (frame.f_code.co_filename, line_number, frame.f_code.co_name)
            for frame, line_number in islice(walk_stack(None), 1, None)
        )

        return throwable

    def get_trace_code(self) -> str:
        """Get a trace code unique to the throwable that is raised.

        The method is concrete, so every throwable gets a trace code without
        writing this body again. `self` still resolves to the class that raised,
        so the code names that class.
        """
        return ThrowableFactory.get_trace_code(self)
