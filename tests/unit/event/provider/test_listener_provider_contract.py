#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ListenerProviderContract."""

import pytest

from tests.fixtures.event.data.listener_fixture import LISTENER_NAME, ListenerFixture
from tests.fixtures.event.provider.listener_provider_fixture import ListenerProviderFixture
from valkyrja.event.provider.contract.listener_provider_contract import ListenerProviderContract


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ListenerProviderContract()  # type: ignore[abstract]


def test_get_listener_classes() -> None:
    assert ListenerProviderFixture().get_listener_classes() == [ListenerFixture]


def test_get_listeners() -> None:
    listeners = ListenerProviderFixture().get_listeners()

    assert [listener.get_name() for listener in listeners] == [LISTENER_NAME]
