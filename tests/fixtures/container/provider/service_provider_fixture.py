#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.container.data.container_data import PublishCallback
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.provider.contract.service_provider_contract import ServiceProviderContract

PROVIDED_ID = "tests.fixtures.container.provider.Provided"
"""The id that `ServiceProviderFixture` publishes."""


@final
class ServiceProviderFixture(ServiceProviderContract):
    """A provider that publishes one singleton."""

    @override
    def publishers(self) -> dict[str, PublishCallback]:
        return {PROVIDED_ID: ServiceProviderFixture.publish_provided}

    @staticmethod
    def publish_provided(container: ContainerContract) -> None:
        container.set_singleton(PROVIDED_ID, {"published": True})
