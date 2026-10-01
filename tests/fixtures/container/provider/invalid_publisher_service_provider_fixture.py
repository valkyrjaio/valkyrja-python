#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, cast, final, override

from valkyrja.container.data.container_data import PublishCallback
from valkyrja.container.provider.contract.service_provider_contract import ServiceProviderContract

INVALID_PROVIDED_ID = "tests.fixtures.container.provider.InvalidProvided"
"""The id that `InvalidPublisherServiceProviderFixture` gives a bad publisher for."""


@final
class InvalidPublisherServiceProviderFixture(ServiceProviderContract):
    """A provider that gives a publisher the container cannot call."""

    @override
    def publishers(self) -> dict[str, PublishCallback]:
        not_a_callable: Any = "this is not a callable"

        return {INVALID_PROVIDED_ID: cast("PublishCallback", not_a_callable)}
