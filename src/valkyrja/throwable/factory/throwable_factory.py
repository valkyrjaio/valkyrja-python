#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from hashlib import md5
from traceback import format_tb


class ThrowableFactory:
    """Builds the values that describe a throwable."""

    @staticmethod
    def get_trace_code(throwable: BaseException) -> str:
        """Get the trace code for a throwable.

        The trace code identifies a failure point, and it identifies nothing
        about a user. The hash is not a security control, so MD5 is sufficient
        and `usedforsecurity` states that.
        """
        cls = type(throwable)
        trace = "".join(format_tb(throwable.__traceback__))

        return md5(f"{cls.__module__}.{cls.__qualname__}{trace}".encode(), usedforsecurity=False).hexdigest()
