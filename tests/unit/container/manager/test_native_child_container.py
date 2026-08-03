#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for NativeChildContainer, which reads the state of a parent Container directly."""

from typing import Any

from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.manager.native_child_container import NativeChildContainer

SERVICE_ID = "tests.unit.container.Service"
SINGLETON_ID = "tests.unit.container.Singleton"
ALIAS_ID = "tests.unit.container.Alias"
CHILD_ID = "tests.unit.container.ChildService"
MISSING_ID = "tests.unit.container.Missing"


def make_service(container: ContainerContract, arguments: dict[str, Any]) -> object:
    return {"arguments": arguments}


def make_parent() -> Container:
    parent = Container()
    parent.bind(SERVICE_ID, make_service)
    parent.bind_alias(ALIAS_ID, SERVICE_ID)
    parent.bind_singleton(SINGLETON_ID, make_service)

    return parent


def test_is_alias_reads_the_child_and_the_parent() -> None:
    child = NativeChildContainer(make_parent())

    assert child.is_alias(ALIAS_ID)
    assert not child.is_alias(MISSING_ID)

    child.bind(CHILD_ID, make_service).bind_alias(CHILD_ID + "Alias", CHILD_ID)

    assert child.is_alias(CHILD_ID + "Alias")


def test_is_service_reads_the_child_and_the_parent() -> None:
    child = NativeChildContainer(make_parent())

    assert child.is_service(SERVICE_ID)
    assert not child.is_service(MISSING_ID)

    child.bind(CHILD_ID, make_service)

    assert child.is_service(CHILD_ID)


def test_is_singleton_binding_reads_the_child_and_the_parent() -> None:
    child = NativeChildContainer(make_parent())

    assert child.is_singleton_binding(SINGLETON_ID)
    assert not child.is_singleton_binding(MISSING_ID)

    child.bind_singleton(CHILD_ID, make_service)

    assert child.is_singleton_binding(CHILD_ID)


def test_is_singleton_instance_reads_the_child_and_the_parent() -> None:
    parent = make_parent()
    parent.get_singleton(SINGLETON_ID)
    child = NativeChildContainer(parent)

    assert child.is_singleton_instance(SINGLETON_ID)
    assert not child.is_singleton_instance(MISSING_ID)

    child.set_singleton(CHILD_ID, object())

    assert child.is_singleton_instance(CHILD_ID)


def test_has_reads_the_child_and_the_parent() -> None:
    parent = make_parent()
    parent.register(ServiceProviderFixture())
    child = NativeChildContainer(parent)

    assert child.has(SERVICE_ID)
    assert child.has(SINGLETON_ID)
    assert child.has(ALIAS_ID)
    assert child.has(PROVIDED_ID)
    assert not child.has(MISSING_ID)

    child.register(ServiceProviderFixture())

    assert child.has(PROVIDED_ID)


def test_is_published_reads_the_child_and_the_parent() -> None:
    child = NativeChildContainer(make_parent())

    assert child.is_published(SERVICE_ID)
    assert not child.is_published(MISSING_ID)

    child.bind(CHILD_ID, make_service)

    assert child.is_published(CHILD_ID)


def test_the_child_reads_a_parent_service() -> None:
    child = NativeChildContainer(make_parent())

    assert child.get(SERVICE_ID, {"key": "value"}) == {"arguments": {"key": "value"}}


def test_the_child_reads_its_own_service_first() -> None:
    child = NativeChildContainer(make_parent())
    child.bind(SERVICE_ID, lambda container, arguments: {"child": True})

    assert child.get(SERVICE_ID) == {"child": True}


def test_the_child_reads_a_parent_singleton_instance() -> None:
    parent = make_parent()
    resolved = parent.get_singleton(SINGLETON_ID)
    child = NativeChildContainer(parent)

    assert child.get_singleton(SINGLETON_ID) is resolved


def test_the_child_reads_its_own_singleton_instance_first() -> None:
    parent = make_parent()
    parent.get_singleton(SINGLETON_ID)
    child = NativeChildContainer(parent)
    own = object()
    child.set_singleton(SINGLETON_ID, own)

    assert child.get_singleton(SINGLETON_ID) is own


def test_the_child_reads_a_parent_alias() -> None:
    child = NativeChildContainer(make_parent())

    assert child.get_aliased(ALIAS_ID) == {"arguments": {}}


def test_the_child_publishes_a_parent_publisher() -> None:
    parent = make_parent()
    parent.register(ServiceProviderFixture())
    child = NativeChildContainer(parent)

    assert not child.is_published(PROVIDED_ID)
    assert child.get_singleton(PROVIDED_ID) == {"published": True}
    assert child.is_published(PROVIDED_ID)


def test_the_child_publishes_its_own_publisher_first() -> None:
    child = NativeChildContainer(make_parent())
    child.register(ServiceProviderFixture())

    assert child.get_singleton(PROVIDED_ID) == {"published": True}


def test_the_child_does_not_publish_an_id_that_no_provider_gives() -> None:
    child = NativeChildContainer(make_parent())

    child.publish(MISSING_ID)

    assert not child.is_published(MISSING_ID)
