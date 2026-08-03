#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from tests.fixtures.event.data.listener_fixture import ListenerFixture
from valkyrja.event.data.contract.listener_contract import ListenerContract
from valkyrja.event.provider.contract.listener_provider_contract import ListenerProviderContract


@final
class ListenerProviderFixture(ListenerProviderContract):
    """A provider that gives one listener class and one listener."""

    @override
    def get_listener_classes(self) -> list[type]:
        return [ListenerFixture]

    @override
    def get_listeners(self) -> list[ListenerContract]:
        return [ListenerFixture()]
