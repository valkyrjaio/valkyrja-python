#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from enum import Enum


class RequestMethod(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    CONNECT = "CONNECT"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PATCH = "PATCH"
    ANY = "ANY"
    """A route that answers every method. A request never carries this one."""

    @classmethod
    def all(cls) -> list[RequestMethod]:
        """Get each method that a request carries.

        `ANY` stands for a route that answers every method, so the list leaves it out.
        """
        return [
            cls.GET,
            cls.HEAD,
            cls.POST,
            cls.PUT,
            cls.DELETE,
            cls.CONNECT,
            cls.OPTIONS,
            cls.TRACE,
            cls.PATCH,
        ]
