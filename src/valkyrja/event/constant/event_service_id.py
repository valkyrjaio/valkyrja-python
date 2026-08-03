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
    """The binding key for each service of the Event component.

    A binding key is a string constant, never a class object. A class object as
    a key forces the module of that class to load. TypeScript holds the same
    keys, because both ports resolve a service by string.
    """

    EVENT_DATA: Final[str] = "Valkyrja.Event.Data.EventData"
    COLLECTION_CONTRACT: Final[str] = "Valkyrja.Event.Collection.ListenerCollectionContract"
    COLLECTOR_CONTRACT: Final[str] = "Valkyrja.Event.Collector.ListenerCollectorContract"
    DISPATCHER_CONTRACT: Final[str] = "Valkyrja.Event.Dispatcher.EventDispatcherContract"
