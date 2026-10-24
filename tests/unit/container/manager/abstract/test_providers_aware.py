#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the ProvidersAware base class, through the Container that extends it."""

import pytest

from tests.fixtures.container.provider.invalid_publisher_service_provider_fixture import (
    InvalidPublisherServiceProviderFixture,
)
from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.manager.abstract.providers_aware import ProvidersAware
from valkyrja.container.manager.container import Container
from valkyrja.container.throwable.exception.container_invalid_publish_callback_exception import (
    ContainerInvalidPublishCallbackException,
)

MISSING_ID = "tests.unit.container.Missing"


def test_the_base_class_does_not_construct() -> None:
    with pytest.raises(TypeError, match="abstract"):
        ProvidersAware()  # type: ignore[abstract]


def test_register_keeps_each_publisher() -> None:
    container = Container()

    container.register(ServiceProviderFixture())

    assert container.has(PROVIDED_ID)
    assert not container.is_published(PROVIDED_ID)


def test_register_raises_for_a_publisher_that_is_no_callable() -> None:
    with pytest.raises(ContainerInvalidPublishCallbackException, match="should have a valid callable"):
        Container().register(InvalidPublisherServiceProviderFixture())


def test_publish_runs_the_publisher() -> None:
    container = Container()
    container.register(ServiceProviderFixture())

    container.publish(PROVIDED_ID)

    assert container.is_published(PROVIDED_ID)
    assert container.get_singleton(PROVIDED_ID) == {"published": True}


def test_publish_does_nothing_for_an_id_that_no_provider_gives() -> None:
    container = Container()

    container.publish(MISSING_ID)

    assert not container.is_published(MISSING_ID)


def test_a_published_service_publishes_once() -> None:
    container = Container()
    container.register(ServiceProviderFixture())

    first = container.get_singleton(PROVIDED_ID)
    second = container.get_singleton(PROVIDED_ID)

    assert first is second
