#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.event.data.contract.listener_contract import ListenerContract


class ListenerProviderContract(ABC):
    """The contract for a provider that gives the listeners of a component.

    Each method returns a plain list, and neither method holds a condition.
    `sindri` reads both lists through the abstract syntax tree, and a condition
    is what stops `sindri` from reading them.
    """

    @abstractmethod
    def get_listener_classes(self) -> list[type]:
        """Get each class that declares a listener with a marker."""

    @abstractmethod
    def get_listeners(self) -> list[ListenerContract]:
        """Get each listener that the provider declares directly."""
