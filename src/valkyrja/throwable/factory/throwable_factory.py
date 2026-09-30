#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from hashlib import md5

type ConstructionFrame = tuple[str, int, str]
"""One frame of a construction stack: the file, the line, and the name."""


class ThrowableFactory:
    @staticmethod
    def get_trace_code(throwable: BaseException) -> str:
        """Get the trace code for a throwable.

        The trace code identifies a failure point, and it identifies nothing
        about a user. The hash is not a security control, so MD5 is sufficient
        and `usedforsecurity` states that.
        """
        cls = type(throwable)
        # A throwable the framework does not define carries no construction stack,
        # so the code names its class alone.
        stack: tuple[ConstructionFrame, ...] = getattr(throwable, "_construction_stack", ())
        frames = "".join(f"{filename}:{line_number}:{name}\n" for filename, line_number, name in stack)

        return md5(f"{cls.__module__}.{cls.__qualname__}{frames}".encode(), usedforsecurity=False).hexdigest()
