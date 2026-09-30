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
from valkyrja.container.throwable.exception.container_unpublished_parent_target_exception import (
    ContainerUnpublishedParentTargetException,
)
from valkyrja.container.throwable.exception.container_unresolved_parent_alias_exception import (
    ContainerUnresolvedParentAliasException,
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


def publish_singleton(container: ContainerContract) -> None:
    container.set_singleton(SINGLETON_ID, {"published": True})


def bind_service(container: ContainerContract) -> None:
    container.bind(SERVICE_ID, make_service)


def make_parent_that_would_publish_a_singleton() -> Container:
    """Get a parent that cached a singleton and then gained a publish callback.

    A cache through `get_singleton` marks nothing published, so the callback of
    the parent still waits to run.
    """
    parent = Container()
    parent.set_from_data(ContainerData(singletons={SINGLETON_ID: SINGLETON_ID}, services={SINGLETON_ID: make_service}))
    parent.get_singleton(SINGLETON_ID)
    parent.set_from_data(ContainerData(callbacks={SINGLETON_ID: publish_singleton}))

    return parent


def make_child_from(parent: Container) -> ChildContainer:
    """Get a child that copies the singletons and the callbacks of the parent."""
    data = parent.get_data()

    return ChildContainer(parent, ContainerData(callbacks=data.callbacks, singletons=data.singletons))


def test_the_child_takes_only_the_singletons_and_the_callbacks_of_the_data() -> None:
    child = ChildContainer(
        Container(), ContainerData(aliases={ALIAS_ID: SERVICE_ID}, services={SERVICE_ID: make_service})
    )

    assert not child.is_alias(ALIAS_ID)
    assert not child.is_service(SERVICE_ID)


def test_get_aliased_id_agrees_with_is_alias() -> None:
    child = ChildContainer(make_parent(), ContainerData())

    assert child.get_aliased_id(ALIAS_ID) == SERVICE_ID
    assert child.get_aliased_id(MISSING_ID) is None


def test_get_aliased_id_reads_the_child_first() -> None:
    parent = make_parent()
    child = ChildContainer(parent, ContainerData())
    child.bind_alias(ALIAS_ID, CHILD_ID)

    assert child.get_aliased_id(ALIAS_ID) == CHILD_ID
    assert parent.get_aliased_id(ALIAS_ID) == SERVICE_ID


def test_get_service_raises_when_the_parent_would_publish() -> None:
    parent = Container()
    parent.set_from_data(ContainerData(callbacks={SERVICE_ID: bind_service}, services={SERVICE_ID: make_service}))
    child = ChildContainer(parent, ContainerData())

    with pytest.raises(ContainerUnpublishedParentTargetException):
        child.get_service(SERVICE_ID)


def test_get_raises_when_the_parent_would_publish_a_singleton() -> None:
    child = ChildContainer(make_parent_that_would_publish_a_singleton(), ContainerData())

    with pytest.raises(ContainerUnpublishedParentTargetException):
        child.get(SINGLETON_ID)


def test_get_singleton_raises_when_nothing_in_the_child_can_answer() -> None:
    child = ChildContainer(make_parent_that_would_publish_a_singleton(), ContainerData())

    with pytest.raises(ContainerUnpublishedParentTargetException):
        child.get_singleton(SINGLETON_ID)


def test_get_prefers_the_alias_of_the_child_over_a_refusal() -> None:
    parent = make_parent_that_would_publish_a_singleton()
    child = ChildContainer(parent, ContainerData())
    child.bind(CHILD_ID, make_service).bind_alias(SINGLETON_ID, CHILD_ID)

    assert child.get(SINGLETON_ID) == {"arguments": {}}
    assert not parent.is_published(SINGLETON_ID)


def test_get_singleton_prefers_the_singleton_binding_of_the_child() -> None:
    parent = make_parent_that_would_publish_a_singleton()
    child = ChildContainer(parent, ContainerData(singletons={SINGLETON_ID: SINGLETON_ID}))
    child.bind(SINGLETON_ID, make_service)

    assert child.get_singleton(SINGLETON_ID) == {"arguments": {}}
    assert not parent.is_published(SINGLETON_ID)


def test_get_prefers_the_binding_of_the_child_over_a_refusal() -> None:
    parent = make_parent_that_would_publish_a_singleton()
    child = ChildContainer(parent, ContainerData())
    child.bind(SINGLETON_ID, make_service)

    assert child.get(SINGLETON_ID) == {"arguments": {}}
    assert not parent.is_published(SINGLETON_ID)


def test_get_service_delegates_when_the_parent_published_already() -> None:
    parent = Container()
    parent.set_from_data(ContainerData(callbacks={SERVICE_ID: bind_service}))
    parent.get(SERVICE_ID)
    child = ChildContainer(parent, ContainerData())

    assert parent.is_published(SERVICE_ID)
    assert child.get_service(SERVICE_ID) == {"arguments": {}}


def test_get_aliased_reuses_a_resolved_parent_singleton() -> None:
    parent = Container()
    resolved = object()
    parent.set_singleton(SINGLETON_ID, resolved)
    parent.bind_alias(ALIAS_ID, SINGLETON_ID)

    assert make_child_from(parent).get_aliased(ALIAS_ID) is resolved


def test_get_aliased_follows_a_parent_alias_chain() -> None:
    parent = Container()
    parent.bind(SERVICE_ID, make_service)
    parent.bind_alias("second", SERVICE_ID)
    parent.bind_alias("first", "second")

    assert make_child_from(parent).get_aliased("first") == {"arguments": {}}


def test_get_aliased_raises_the_error_of_the_parent_for_an_absent_target() -> None:
    parent = Container()
    parent.bind_alias(ALIAS_ID, SERVICE_ID)

    with pytest.raises(ContainerInvalidReferenceException):
        make_child_from(parent).get_aliased(ALIAS_ID)


def test_get_aliased_resolves_a_self_alias_in_the_parent() -> None:
    parent = Container()
    parent.bind(SERVICE_ID, make_service)
    parent.bind_alias(SERVICE_ID, SERVICE_ID)

    assert make_child_from(parent).get_aliased(SERVICE_ID) == {"arguments": {}}


def test_get_aliased_stops_on_a_cyclic_parent_alias_chain() -> None:
    parent = Container()
    parent.bind_alias("first", "second")
    parent.bind_alias("second", "first")

    with pytest.raises(ContainerInvalidReferenceException):
        make_child_from(parent).get_aliased("first")


def test_get_aliased_raises_for_an_unresolved_singleton_part_way_along_the_chain() -> None:
    parent = Container()
    parent.bind_alias("outer", "middle")
    parent.bind_singleton("middle", make_service)
    parent.bind_alias("middle", SERVICE_ID)
    parent.bind(SERVICE_ID, make_service)

    with pytest.raises(ContainerUnresolvedParentAliasException):
        make_child_from(parent).get_aliased("outer")


def test_get_aliased_raises_for_a_target_held_as_both_callback_and_alias() -> None:
    parent = Container()
    parent.register(ServiceProviderFixture())
    parent.bind_alias("outer", PROVIDED_ID)
    parent.bind_alias(PROVIDED_ID, SINGLETON_ID)

    with pytest.raises(ContainerUnresolvedParentAliasException):
        make_child_from(parent).get_aliased("outer")


def test_get_aliased_raises_for_an_unresolved_parent_singleton() -> None:
    parent = Container()
    parent.bind_singleton(SINGLETON_ID, make_service)
    parent.bind_alias(ALIAS_ID, SINGLETON_ID)

    with pytest.raises(ContainerUnresolvedParentAliasException):
        make_child_from(parent).get_aliased(ALIAS_ID)


def test_get_aliased_raises_for_an_unpublished_parent_target() -> None:
    parent = Container()
    parent.register(ServiceProviderFixture())
    parent.bind_alias(ALIAS_ID, PROVIDED_ID)

    with pytest.raises(ContainerUnresolvedParentAliasException):
        make_child_from(parent).get_aliased(ALIAS_ID)


def test_get_aliased_names_the_hop_it_stopped_at() -> None:
    parent = Container()
    parent.bind_alias("first", "second")
    parent.bind_alias("second", SINGLETON_ID)
    parent.bind_singleton(SINGLETON_ID, make_service)

    with pytest.raises(ContainerUnresolvedParentAliasException, match=f"Alias `first` reaches `{SINGLETON_ID}`"):
        make_child_from(parent).get_aliased("first")


def test_get_aliased_delegates_when_the_parent_published_already() -> None:
    parent = Container()
    parent.register(ServiceProviderFixture())
    parent.get(PROVIDED_ID)
    parent.bind_alias(ALIAS_ID, PROVIDED_ID)

    assert parent.is_published(PROVIDED_ID)
    assert make_child_from(parent).get_aliased(ALIAS_ID) == {"published": True}


def test_is_deferred_reports_only_the_callbacks_of_the_child() -> None:
    parent = Container()
    parent.register(ServiceProviderFixture())
    child = ChildContainer(parent, ContainerData())

    # `has` reads `is_deferred`, so a true here would promise a `get` that fails.
    assert not child.is_deferred(PROVIDED_ID)
    assert not child.has(PROVIDED_ID)


def test_is_deferred_reads_the_callbacks_that_the_data_copied() -> None:
    parent = Container()
    parent.register(ServiceProviderFixture())
    child = make_child_from(parent)

    assert child.is_deferred(PROVIDED_ID)
    assert not child.is_deferred(SINGLETON_ID)


def test_the_parent_keeps_its_state_after_the_child_resolves() -> None:
    parent = make_parent()
    parent.register(ServiceProviderFixture())
    child = make_child_from(parent)
    data_before = parent.get_data()
    singleton_instance_before = parent.is_singleton_instance(SINGLETON_ID)

    child.get(SERVICE_ID)
    child.get_service(SERVICE_ID)
    child.get_aliased(ALIAS_ID)
    child.get_singleton(SINGLETON_ID)
    child.get(PROVIDED_ID)

    data_after = parent.get_data()

    assert data_before == data_after
    assert parent.is_singleton_instance(SINGLETON_ID) == singleton_instance_before
    assert not parent.is_published(PROVIDED_ID)
