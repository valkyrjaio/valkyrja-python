#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Container manager."""

from typing import Any

import pytest

from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.data.container_data import ContainerData
from valkyrja.container.enum.invalid_reference_mode import InvalidReferenceMode
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
)

SERVICE_ID = "tests.unit.container.Service"
SINGLETON_ID = "tests.unit.container.Singleton"
ALIAS_ID = "tests.unit.container.Alias"
MISSING_ID = "tests.unit.container.Missing"


def make_service(container: ContainerContract, arguments: dict[str, Any]) -> object:
    return {"arguments": arguments}


def test_a_new_container_has_nothing() -> None:
    container = Container()

    assert not container.has(SERVICE_ID)
    assert not container.is_alias(SERVICE_ID)
    assert not container.is_service(SERVICE_ID)
    assert not container.is_singleton(SERVICE_ID)
    assert not container.is_singleton_binding(SERVICE_ID)
    assert not container.is_singleton_instance(SERVICE_ID)


def test_a_container_takes_data() -> None:
    container = Container(ContainerData(aliases={ALIAS_ID: SERVICE_ID}, services={SERVICE_ID: make_service}))

    assert container.is_alias(ALIAS_ID)
    assert container.is_service(SERVICE_ID)


def test_bind_registers_a_service() -> None:
    container = Container()

    assert container.bind(SERVICE_ID, make_service) is container
    assert container.is_service(SERVICE_ID)
    assert container.has(SERVICE_ID)
    assert container.is_published(SERVICE_ID)


def test_bind_alias_registers_an_alias() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    assert container.bind_alias(ALIAS_ID, SERVICE_ID) is container
    assert container.is_alias(ALIAS_ID)
    assert container.has(ALIAS_ID)


def test_bind_singleton_registers_a_singleton_binding() -> None:
    container = Container()

    assert container.bind_singleton(SINGLETON_ID, make_service) is container
    assert container.is_singleton_binding(SINGLETON_ID)
    assert container.is_singleton(SINGLETON_ID)
    assert not container.is_singleton_instance(SINGLETON_ID)


def test_set_singleton_registers_an_instance() -> None:
    container = Container()
    singleton = object()

    assert container.set_singleton(SINGLETON_ID, singleton) is container
    assert container.is_singleton_instance(SINGLETON_ID)
    assert container.is_singleton(SINGLETON_ID)
    assert container.get_singleton(SINGLETON_ID) is singleton


def test_get_builds_a_service_each_time() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    assert container.get(SERVICE_ID) is not container.get(SERVICE_ID)


def test_get_passes_the_arguments_to_the_factory() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    assert container.get(SERVICE_ID, {"key": "value"}) == {"arguments": {"key": "value"}}


def test_get_builds_a_singleton_once() -> None:
    container = Container().bind_singleton(SINGLETON_ID, make_service)

    assert container.get(SINGLETON_ID) is container.get(SINGLETON_ID)
    assert container.is_singleton_instance(SINGLETON_ID)


def test_get_reads_an_alias() -> None:
    container = Container().bind(SERVICE_ID, make_service).bind_alias(ALIAS_ID, SERVICE_ID)

    assert container.get(ALIAS_ID) == {"arguments": {}}


def test_get_raises_for_a_missing_id() -> None:
    with pytest.raises(ContainerInvalidReferenceException, match="not found"):
        Container().get(MISSING_ID)


def test_get_raises_for_a_missing_id_in_the_throw_mode() -> None:
    with pytest.raises(ContainerInvalidReferenceException):
        Container().get(MISSING_ID, {}, InvalidReferenceMode.THROW_EXCEPTION)


def test_get_returns_a_service_that_is_false() -> None:
    """A falsy service resolves. PHP chains with `??`, and Python must not use `or`."""
    container = Container().bind(SERVICE_ID, lambda container, arguments: [])

    assert container.get(SERVICE_ID) == []


def test_get_aliased_raises_when_the_id_is_no_alias() -> None:
    with pytest.raises(ContainerInvalidReferenceException):
        Container().get_aliased(MISSING_ID)


def test_get_aliased_passes_the_arguments() -> None:
    container = Container().bind(SERVICE_ID, make_service).bind_alias(ALIAS_ID, SERVICE_ID)

    assert container.get_aliased(ALIAS_ID, {"key": "value"}) == {"arguments": {"key": "value"}}


def test_get_service_returns_the_service() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    assert container.get_service(SERVICE_ID, {"key": "value"}) == {"arguments": {"key": "value"}}


def test_get_service_raises_for_a_missing_id() -> None:
    with pytest.raises(ContainerInvalidReferenceException):
        Container().get_service(MISSING_ID)


def test_get_singleton_raises_for_a_missing_id() -> None:
    with pytest.raises(ContainerInvalidReferenceException):
        Container().get_singleton(MISSING_ID)


def test_get_singleton_raises_for_a_binding_with_no_service() -> None:
    """A binding with no factory resolves to nothing, so the container raises."""
    container = Container(ContainerData(singletons={SINGLETON_ID: SINGLETON_ID}))

    assert container.is_singleton_binding(SINGLETON_ID)

    with pytest.raises(ContainerInvalidReferenceException):
        container.get_singleton(SINGLETON_ID)


def test_get_data_returns_the_state() -> None:
    container = Container().bind_singleton(SINGLETON_ID, make_service).bind_alias(ALIAS_ID, SINGLETON_ID)
    container.register(ServiceProviderFixture())

    data = container.get_data()

    assert data.aliases == {ALIAS_ID: SINGLETON_ID}
    assert data.services == {SINGLETON_ID: make_service}
    assert data.singletons == {SINGLETON_ID: SINGLETON_ID}
    assert PROVIDED_ID in data.callbacks


def test_get_data_copies_the_state() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    container.get_data().services.clear()

    assert container.is_service(SERVICE_ID)


def test_set_from_data_adds_to_the_state() -> None:
    container = Container().bind(SERVICE_ID, make_service)

    container.set_from_data(
        ContainerData(
            aliases={ALIAS_ID: SERVICE_ID},
            services={SINGLETON_ID: make_service},
            singletons={SINGLETON_ID: SINGLETON_ID},
        )
    )

    assert container.is_service(SERVICE_ID)
    assert container.is_alias(ALIAS_ID)
    assert container.is_singleton_binding(SINGLETON_ID)


def test_has_reads_a_publisher() -> None:
    container = Container()
    container.register(ServiceProviderFixture())

    assert container.has(PROVIDED_ID)


def test_get_publishes_a_provided_service() -> None:
    container = Container()
    container.register(ServiceProviderFixture())

    assert not container.is_published(PROVIDED_ID)
    assert container.get(PROVIDED_ID) == {"published": True}
    assert container.is_published(PROVIDED_ID)
