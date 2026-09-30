#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, override

from valkyrja.container.data.container_data import ContainerData
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


class ChildContainer(Container):
    def __init__(self, parent: ContainerContract, data: ContainerData) -> None:
        super().__init__()

        # Only the singletons and the callbacks come from the data. An alias or a
        # service would make the child resolve what the parent owns, and the
        # parent caches what it resolves, so the child would write to the parent.
        self._parent = parent
        self._singletons = dict(data.singletons)
        self._callbacks.update(data.callbacks)

    @override
    def is_alias(self, id_: str) -> bool:
        return super().is_alias(id_) or self._parent.is_alias(id_)

    @override
    def get_aliased_id(self, alias: str) -> str | None:
        # Warning: the lookup tests for `None`, never for a false value. An empty
        # alias is a false value, so `or` would read past it to the parent.
        aliased_id = super().get_aliased_id(alias)

        return aliased_id if aliased_id is not None else self._parent.get_aliased_id(alias)

    @override
    def is_service(self, id_: str) -> bool:
        return super().is_service(id_) or self._parent.is_service(id_)

    @override
    def is_singleton_instance(self, id_: str) -> bool:
        return super().is_singleton_instance(id_) or self._parent.is_singleton_instance(id_)

    @override
    def is_published(self, id_: str) -> bool:
        return super().is_published(id_) or self._parent.is_published(id_)

    @override
    def _get_singleton_without_checks(self, id_: str) -> object | None:
        # The parent holds a resolved instance, and the child holds none of its own.
        if not super().is_singleton_instance(id_) and self._parent.is_singleton_instance(id_):
            if self._is_unpublished_in_parent(id_):
                # Delegating would run the publish callback of the parent, so the
                # child answers instead.
                instance = super()._get_singleton_without_checks(id_)

                if instance is not None:
                    return instance

                # `get` tries the service and the alias maps of the child after
                # this, and `get_singleton` does not, so refusing waits until
                # neither can answer.
                if super().is_service(id_) or super().is_alias(id_):
                    return None

                raise ContainerUnpublishedParentTargetException(id_)

            return self._parent.get_singleton(id_)

        return super()._get_singleton_without_checks(id_)

    @override
    def _get_service_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        if not super().is_service(id_) and self._parent.is_service(id_):
            if self._is_unpublished_in_parent(id_):
                # `get` tries the alias map of the child after this, and
                # `get_service` does not, so refusing waits until that cannot answer.
                if super().is_alias(id_):
                    return None

                raise ContainerUnpublishedParentTargetException(id_)

            return self._parent.get_service(id_, arguments)

        return super()._get_service_without_checks(id_, arguments)

    @override
    def _get_aliased_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        if super().is_alias(id_):
            return super()._get_aliased_without_checks(id_, arguments)

        if not self._parent.is_alias(id_):
            return None

        self._validate_parent_alias_resolution(id_)

        return self._parent.get_aliased(id_, arguments)

    def _is_unpublished_in_parent(self, id_: str) -> bool:
        """Get whether the parent holds a publish callback it has not run."""
        return self._parent.is_deferred(id_) and not self._parent.is_published(id_)

    def _validate_parent_alias_resolution(self, id_: str) -> None:
        """Check that the parent answers an alias without caching anything new."""
        seen: set[str] = set()
        current = id_

        while (aliased_id := self._parent.get_aliased_id(current)) is not None:
            if aliased_id in seen:
                raise ContainerInvalidReferenceException(id_)

            seen.add(aliased_id)
            current = aliased_id

            if self._is_unresolved_in_parent(current):
                raise ContainerUnresolvedParentAliasException(id_, current)

            # The parent answers a singleton or a service before it follows an
            # alias, so it never reaches the rest of the chain.
            if self._parent.is_singleton_instance(current) or self._parent.is_service(current):
                return

    def _is_unresolved_in_parent(self, id_: str) -> bool:
        """Get whether the parent would cache a given id for the first time."""
        # The parent publishes before it reads any map, so this test comes first.
        if self._is_unpublished_in_parent(id_):
            return True

        if self._parent.is_singleton_instance(id_):
            return False

        return self._parent.is_singleton_binding(id_)
