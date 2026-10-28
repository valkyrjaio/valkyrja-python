#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from typing import Any, Self, override

from valkyrja.container.data.container_data import ContainerData, ServiceFactory
from valkyrja.container.manager.abstract.providers_aware import ProvidersAware
from valkyrja.container.throwable.exception.container_cyclic_alias_exception import (
    ContainerCyclicAliasException,
)
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
)


class Container(ProvidersAware):
    def __init__(self, data: ContainerData | None = None) -> None:
        super().__init__()

        data = data if data is not None else ContainerData()

        # Nothing is installed before the walks end.
        self._validate_alias_map_is_not_cyclic(data.aliases, lambda id_: None)

        self._aliases: dict[str, str] = dict(data.aliases)
        self._instances: dict[str, object] = {}
        self._services: dict[str, ServiceFactory] = dict(data.services)
        self._singletons: dict[str, str] = dict(data.singletons)
        self._callbacks.update(data.callbacks)

    @override
    def get_data(self) -> ContainerData:
        return ContainerData(
            aliases=dict(self._aliases),
            callbacks=dict(self._callbacks),
            services=dict(self._services),
            singletons=dict(self._singletons),
        )

    @override
    def set_from_data(self, data: ContainerData) -> None:
        self._validate_alias_map_is_not_cyclic(data.aliases, self.get_aliased_id)

        self._aliases.update(data.aliases)
        self._callbacks.update(data.callbacks)
        self._services.update(data.services)
        self._singletons.update(data.singletons)

    @override
    def has(self, id_: str) -> bool:
        return self.is_deferred(id_) or self.is_singleton(id_) or self.is_service(id_) or self.is_alias(id_)

    @override
    def bind(self, id_: str, factory: ServiceFactory) -> Self:
        self._services[id_] = factory
        self._published[id_] = True

        return self

    @override
    def bind_alias(self, alias: str, id_: str) -> Self:
        self._validate_alias_is_not_cyclic(alias, id_)

        self._aliases[alias] = id_

        return self

    @override
    def bind_singleton(self, id_: str, factory: ServiceFactory) -> Self:
        self._singletons[id_] = id_
        self.bind(id_, factory)

        return self

    @override
    def set_singleton(self, id_: str, singleton: object) -> Self:
        self._instances[id_] = singleton
        self._published[id_] = True

        return self

    @override
    def is_alias(self, id_: str) -> bool:
        return id_ in self._aliases

    @override
    def get_aliased_id(self, alias: str) -> str | None:
        return self._aliases.get(alias)

    def _validate_alias_is_not_cyclic(self, alias: str, id_: str) -> None:
        """Refuse an alias whose chain returns to the alias itself."""
        if alias == id_:
            raise ContainerCyclicAliasException(alias, id_)

        seen: set[str] = set()
        current = id_

        while (aliased_id := self.get_aliased_id(current)) is not None:
            if aliased_id == alias:
                raise ContainerCyclicAliasException(alias, id_)

            # A parent that binds an alias after a child is built checks only its
            # own map, so the two can hold a cycle this alias is no part of. End
            # the walk there.
            if aliased_id in seen:
                return

            seen.add(aliased_id)
            current = aliased_id

    @staticmethod
    def _validate_alias_map_is_not_cyclic(aliases: dict[str, str], installed: Callable[[str], str | None]) -> None:
        """Refuse an alias map that holds a chain returning to its own start.

        `installed` reads an id the map does not name, so a chain that closes
        through what the container already reaches is refused as well. A child
        reaches the aliases of its parent, which the map alone never names.
        """
        for alias in aliases:
            seen = {alias}
            current = alias

            while True:
                # Warning: each read tests for `None`, never for a false value. An
                # empty id is a false value, so `or` would read past it.
                aliased_id = aliases.get(current)

                if aliased_id is None:
                    aliased_id = installed(current)

                if aliased_id is None:
                    break

                # Name the edge that took the walk back to its start.
                if aliased_id == alias:
                    raise ContainerCyclicAliasException(current, aliased_id)

                # A chain the container already held ends its walk here, the same way
                # `bind_alias` ends its own.
                if aliased_id in seen:
                    break

                seen.add(aliased_id)
                current = aliased_id

    @override
    def is_service(self, id_: str) -> bool:
        return id_ in self._services

    @override
    def is_singleton(self, id_: str) -> bool:
        return self.is_singleton_binding(id_) or self.is_singleton_instance(id_)

    @override
    def is_singleton_binding(self, id_: str) -> bool:
        return id_ in self._singletons

    @override
    def is_singleton_instance(self, id_: str) -> bool:
        return id_ in self._instances

    @override
    def get(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        arguments = arguments if arguments is not None else {}

        self._publish_unpublished_provided(id_)

        # Warning: each step tests for `None`, never for a false value. An empty
        # service is a false value, so `or` would fall through to the next step.
        singleton = self._get_singleton_without_checks(id_)

        if singleton is not None:
            return singleton

        service = self._get_service_without_checks(id_, arguments)

        if service is not None:
            return service

        aliased = self._get_aliased_without_checks(id_, arguments)

        if aliased is not None:
            return aliased

        raise ContainerInvalidReferenceException(id_)

    @override
    def get_aliased(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        aliased = self._get_aliased_without_checks(id_, arguments if arguments is not None else {})

        if aliased is None:
            raise ContainerInvalidReferenceException(id_)

        return aliased

    @override
    def get_service(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        self._publish_unpublished_provided(id_)

        service = self._get_service_without_checks(id_, arguments if arguments is not None else {})

        if service is None:
            raise ContainerInvalidReferenceException(id_)

        return service

    @override
    def get_singleton(self, id_: str) -> object:
        self._publish_unpublished_provided(id_)

        singleton = self._get_singleton_without_checks(id_)

        if singleton is None:
            raise ContainerInvalidReferenceException(id_)

        return singleton

    def _get_aliased_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        """Get the service that an alias points to, without a publish step."""
        aliased = self.get_aliased_id(id_)

        if aliased is None:
            return None

        return self.get(aliased, arguments)

    def _get_singleton_without_checks(self, id_: str) -> object | None:
        """Get a singleton, without an alias step and without a publish step."""
        instance = self._get_singleton_instance(id_)

        if instance is not None:
            return instance

        if not self.is_singleton_binding(id_):
            return None

        singleton = self._get_service_without_checks(id_, {})

        if singleton is None:
            return None

        # The map decides which instance every reader gets, because a factory can
        # cache an instance for this id while it runs, before this write.
        cached = self._instances.get(id_)

        if cached is not None:
            return cached

        self._instances[id_] = singleton

        return singleton

    def _get_service_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        """Get a service, without an alias step and without a publish step."""
        factory = self._get_service_factory(id_)

        if factory is None:
            return None

        return factory(self, arguments)

    def _get_singleton_instance(self, id_: str) -> object | None:
        """Get the singleton instance that the container holds for an id."""
        return self._instances.get(id_)

    def _get_service_factory(self, id_: str) -> ServiceFactory | None:
        """Get the factory that the container holds for an id."""
        return self._services.get(id_)
