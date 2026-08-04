#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ServiceProviderContract."""

import pytest

from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.manager.container import Container
from valkyrja.container.provider.contract.service_provider_contract import ServiceProviderContract


def test_the_contract_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ServiceProviderContract()  # type: ignore[abstract]


def test_publishers_names_each_provided_service() -> None:
    publishers = ServiceProviderFixture().publishers()

    assert list(publishers) == [PROVIDED_ID]


def test_a_publisher_binds_the_service() -> None:
    container = Container()

    ServiceProviderFixture.publish_provided(container)

    assert container.get_singleton(PROVIDED_ID) == {"published": True}
