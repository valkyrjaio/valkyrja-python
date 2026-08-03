#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.container.provider.contract.service_provider_contract import ServiceProviderContract


class ProvidersAwareContract(ABC):
    """The contract for a container that registers and publishes a provider."""

    @abstractmethod
    def register(self, provider: ServiceProviderContract) -> None:
        """Register a provider, and keep each publisher that the provider gives."""

    @abstractmethod
    def is_published(self, id_: str) -> bool:
        """Get whether the container published the service for a given id."""

    @abstractmethod
    def publish(self, id_: str) -> None:
        """Publish the service for a given id.

        The method does nothing when no provider gives that id.
        """
