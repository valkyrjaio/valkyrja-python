#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC
from typing import override

from valkyrja.container.data.container_data import PublishCallback
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.provider.contract.service_provider_contract import ServiceProviderContract
from valkyrja.container.throwable.exception.container_invalid_publish_callback_exception import (
    ContainerInvalidPublishCallbackException,
)


# The base is `ContainerContract`, which already extends `ProvidersAwareContract`.
# Java names both, because Java linearizes no interface. Python does linearize,
# and naming both raises `TypeError: Cannot create a consistent method resolution
# order`, because `ContainerContract` already orders one before the other.
class ProvidersAware(ContainerContract, ABC):
    """Holds the publisher that each provider gives, and publishes it once.

    PHP mixes this behavior in with a trait. Python has no trait, so the
    behavior is a base class that `Container` extends, the same as Java.
    """

    def __init__(self) -> None:
        self._callbacks: dict[str, PublishCallback] = {}
        self._published: dict[str, bool] = {}

    @override
    def register(self, provider: ServiceProviderContract) -> None:
        for provided, publish_callback in provider.publishers().items():
            if not callable(publish_callback):
                raise ContainerInvalidPublishCallbackException(f"{provided} should have a valid callable")

            self._callbacks[provided] = publish_callback

    @override
    def is_published(self, id_: str) -> bool:
        return id_ in self._published

    @override
    def publish(self, id_: str) -> None:
        publish_callback = self._get_callback(id_)

        if publish_callback is None:
            return

        publish_callback(self)

        self._published[id_] = True

    def _get_callback(self, id_: str) -> PublishCallback | None:
        """Get the publisher for a given id."""
        return self._callbacks.get(id_)

    def _publish_unpublished_provided(self, id_: str) -> None:
        """Publish the service for a given id, unless the container published it already."""
        if id_ in self._callbacks and not self.is_published(id_):
            self.publish(id_)
