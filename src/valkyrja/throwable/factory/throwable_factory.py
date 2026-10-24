#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from hashlib import md5

# One frame of a construction stack: the file, the line, and the name.
type ConstructionFrame = tuple[str, int, str]


class ThrowableFactory:
    @staticmethod
    def get_trace_code(throwable: BaseException) -> str:
        """Get the trace code for a throwable."""
        cls = type(throwable)
        # A throwable carries no construction stack when the framework does not define
        # it, and when its base list defeats the guard. The code then names its class
        # alone, so every instance of that class shares one code.
        stack: tuple[ConstructionFrame, ...] = getattr(throwable, "_construction_stack", ())
        frames = "".join(f"{filename}:{line_number}:{name}\n" for filename, line_number, name in stack)

        # The code identifies a failure point, never a user, so the hash is not a
        # security control and `usedforsecurity` states that.
        return md5(f"{cls.__module__}.{cls.__qualname__}{frames}".encode(), usedforsecurity=False).hexdigest()
