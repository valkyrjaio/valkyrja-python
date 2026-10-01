#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Final, final


@final
class EventServiceId:
    EVENT_DATA: Final[str] = "valkyrja.event.data.EventData"
    COLLECTION_CONTRACT: Final[str] = "valkyrja.event.collection.ListenerCollectionContract"
    COLLECTOR_CONTRACT: Final[str] = "valkyrja.event.collector.ListenerCollectorContract"
    DISPATCHER_CONTRACT: Final[str] = "valkyrja.event.dispatcher.EventDispatcherContract"
