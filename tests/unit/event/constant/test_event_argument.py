#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the argument key of the Event component."""

from valkyrja.event.constant.event_argument import EVENT_ARGUMENT_KEY


def test_the_event_argument_key() -> None:
    assert EVENT_ARGUMENT_KEY == "event"
