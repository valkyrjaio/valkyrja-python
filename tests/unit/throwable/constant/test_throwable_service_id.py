#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ThrowableServiceId.

Each key is part of the public API, so each test pins the whole string. The
TypeScript port holds the same keys.
"""

from valkyrja.throwable.constant.throwable_service_id import ThrowableServiceId


def test_handler_contract() -> None:
    assert ThrowableServiceId.HANDLER_CONTRACT == "Valkyrja.Throwable.Handler.ThrowableHandlerContract"
