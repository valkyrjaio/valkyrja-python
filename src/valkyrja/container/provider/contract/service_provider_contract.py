#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod

from valkyrja.container.data.container_data import PublishCallback


class ServiceProviderContract(ABC):
    """The contract for a provider that publishes a service to the container."""

    @abstractmethod
    def publishers(self) -> dict[str, PublishCallback]:
        """Get the publisher for each service that this provider gives.

        The container calls a publisher the first time an application asks for
        that service. A publisher is a plain method reference, and the method
        binds the service:

        ```python
        class ContainerServiceProvider(ServiceProviderContract):
            @override
            def publishers(self) -> dict[str, PublishCallback]:
                return {ContainerServiceId.DATA: ContainerServiceProvider.publish_data}

            @staticmethod
            def publish_data(container: ContainerContract) -> None:
                container.set_singleton(ContainerServiceId.DATA, container.get_data())
        ```
        """
