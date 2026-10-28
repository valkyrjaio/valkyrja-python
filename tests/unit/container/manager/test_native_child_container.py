#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for NativeChildContainer, which reads the state of a parent Container directly."""

from typing import Any

import pytest

from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.data.container_data import ContainerData
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.manager.native_child_container import NativeChildContainer
from valkyrja.container.throwable.exception.container_cyclic_alias_exception import (
    ContainerCyclicAliasException,
)

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


def test_is_deferred_reads_the_child_and_the_parent() -> None:
    parent = make_parent()
    parent.register(ServiceProviderFixture())
    child = NativeChildContainer(parent)

    assert child.is_deferred(PROVIDED_ID)
    assert not child.is_deferred(MISSING_ID)

    own = NativeChildContainer(make_parent())
    own.register(ServiceProviderFixture())

    assert own.is_deferred(PROVIDED_ID)


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


def test_set_from_data_refuses_an_alias_that_closes_a_cycle_through_the_parent() -> None:
    parent = Container()
    parent.bind_alias("first", "second")
    child = NativeChildContainer(parent)

    with pytest.raises(ContainerCyclicAliasException, match="returns to"):
        child.set_from_data(ContainerData(aliases={"second": "first"}))


def test_set_from_data_takes_an_alias_that_closes_no_cycle_through_the_parent() -> None:
    parent = Container()
    parent.bind(SERVICE_ID, make_service)
    parent.bind_alias("first", SERVICE_ID)
    child = NativeChildContainer(parent)

    child.set_from_data(ContainerData(aliases={"second": "first"}))

    assert child.get("second") == {"arguments": {}}


def test_set_from_data_refuses_two_loaded_aliases_that_close_a_cycle_through_the_parent() -> None:
    parent = Container()
    parent.bind_alias("b", "c")
    child = NativeChildContainer(parent)

    # Neither alias closes the cycle on its own. The chain runs through the parent,
    # which the loaded map never names.
    with pytest.raises(ContainerCyclicAliasException):
        child.set_from_data(ContainerData(aliases={"a": "b", "c": "a"}))


def test_bind_alias_ends_the_walk_on_a_cycle_that_a_parent_closed_after_the_child() -> None:
    parent = Container()
    parent.bind_alias("b", "c")
    child = NativeChildContainer(parent)
    child.bind_alias("a", "b")
    # The parent reads only its own map, so it takes the edge that closes the chain.
    parent.bind_alias("c", "a")

    # The new alias is no part of that cycle, so the walk ends rather than running on.
    assert child.bind_alias("x", "a") is child
