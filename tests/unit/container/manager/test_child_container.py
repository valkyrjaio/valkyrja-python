#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for ChildContainer, which reads a parent through the contract."""

from typing import Any

import pytest

from tests.fixtures.container.provider.service_provider_fixture import (
    PROVIDED_ID,
    ServiceProviderFixture,
)
from valkyrja.container.data.container_data import ContainerData
from valkyrja.container.manager.child_container import ChildContainer
from valkyrja.container.manager.container import Container
from valkyrja.container.manager.contract.container_contract import ContainerContract
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
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


def test_is_alias_reads_the_child_first() -> None:
    child = ChildContainer(make_parent(), ContainerData())
    child.bind(CHILD_ID, make_service).bind_alias(CHILD_ID + "Alias", CHILD_ID)

    assert child.is_alias(CHILD_ID + "Alias")


def test_is_alias_reads_the_parent() -> None:
    child = ChildContainer(make_parent(), ContainerData())

    assert child.is_alias(ALIAS_ID)
    assert not child.is_alias(MISSING_ID)


def test_is_service_reads_the_child_and_the_parent() -> None:
    child = ChildContainer(make_parent(), ContainerData())
    child.bind(CHILD_ID, make_service)

    assert child.is_service(CHILD_ID)
    assert child.is_service(SERVICE_ID)
    assert not child.is_service(MISSING_ID)


def test_is_singleton_instance_reads_the_child_and_the_parent() -> None:
    parent = make_parent()
    parent.get_singleton(SINGLETON_ID)
    child = ChildContainer(parent, ContainerData())

    assert child.is_singleton_instance(SINGLETON_ID)

    child.set_singleton(CHILD_ID, object())

    assert child.is_singleton_instance(CHILD_ID)
    assert not child.is_singleton_instance(MISSING_ID)


def test_is_published_reads_the_child_and_the_parent() -> None:
    parent = make_parent()
    child = ChildContainer(parent, ContainerData())

    assert child.is_published(SERVICE_ID)

    child.bind(CHILD_ID, make_service)

    assert child.is_published(CHILD_ID)
    assert not child.is_published(MISSING_ID)


def test_the_child_reuses_a_resolved_parent_singleton() -> None:
    parent = make_parent()
    resolved = parent.get_singleton(SINGLETON_ID)
    child = ChildContainer(parent, ContainerData())

    assert child.get_singleton(SINGLETON_ID) is resolved


def test_the_child_builds_its_own_singleton_from_a_local_binding() -> None:
    parent = make_parent()
    child = ChildContainer(parent, ContainerData(singletons={SINGLETON_ID: SINGLETON_ID}))
    child.bind(SINGLETON_ID, make_service)

    child_singleton = child.get_singleton(SINGLETON_ID)

    assert child_singleton is not parent.get_singleton(SINGLETON_ID)


def test_the_child_reads_a_parent_service() -> None:
    child = ChildContainer(make_parent(), ContainerData())

    assert child.get_service(SERVICE_ID, {"key": "value"}) == {"arguments": {"key": "value"}}


def test_the_child_reads_its_own_service_first() -> None:
    child = ChildContainer(make_parent(), ContainerData())
    child.bind(SERVICE_ID, lambda container, arguments: {"child": True})

    assert child.get_service(SERVICE_ID) == {"child": True}


def test_the_child_reads_a_parent_alias() -> None:
    child = ChildContainer(make_parent(), ContainerData())

    assert child.get_aliased(ALIAS_ID) == {"arguments": {}}


def test_the_child_reads_its_own_alias_first() -> None:
    child = ChildContainer(make_parent(), ContainerData())
    child.bind(CHILD_ID, lambda container, arguments: {"child": True}).bind_alias(ALIAS_ID, CHILD_ID)

    assert child.get_aliased(ALIAS_ID) == {"child": True}


def test_the_child_takes_the_publishers_of_the_data() -> None:
    child = ChildContainer(make_parent(), ContainerData(callbacks=ServiceProviderFixture().publishers()))

    assert child.get_singleton(PROVIDED_ID) == {"published": True}


def test_the_child_raises_for_a_missing_id() -> None:
    child = ChildContainer(make_parent(), ContainerData())

    with pytest.raises(ContainerInvalidReferenceException):
        child.get(MISSING_ID)
