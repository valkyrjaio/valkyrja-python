#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, Self, override

from valkyrja.container.data.container_data import ContainerData, ServiceFactory
from valkyrja.container.enum.invalid_reference_mode import InvalidReferenceMode
from valkyrja.container.manager.abstract.providers_aware import ProvidersAware
from valkyrja.container.throwable.exception.container_invalid_reference_exception import (
    ContainerInvalidReferenceException,
)


class Container(ProvidersAware):
    """The service container.

    The container resolves an id in one order: a singleton, then a service, then
    an alias, then the fallback.
    """

    def __init__(self, data: ContainerData | None = None) -> None:
        super().__init__()

        data = data if data is not None else ContainerData()

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
        self._aliases.update(data.aliases)
        self._callbacks.update(data.callbacks)
        self._services.update(data.services)
        self._singletons.update(data.singletons)

    @override
    def has(self, id_: str) -> bool:
        return id_ in self._callbacks or self.is_singleton(id_) or self.is_service(id_) or self.is_alias(id_)

    @override
    def bind(self, id_: str, factory: ServiceFactory) -> Self:
        self._services[id_] = factory
        self._published[id_] = True

        return self

    @override
    def bind_alias(self, alias: str, id_: str) -> Self:
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
    def get(
        self,
        id_: str,
        arguments: dict[str, Any] | None = None,
        mode: InvalidReferenceMode = InvalidReferenceMode.NEW_INSTANCE_OR_THROW_EXCEPTION,
    ) -> object:
        arguments = arguments if arguments is not None else {}

        self._publish_unpublished_provided(id_)

        # Warning: each step tests for `None`, never for a false value. PHP
        # chains these with `??`, which tests for null alone. Python's `or`
        # tests for a false value, so an empty service would fall through to
        # the next step.
        singleton = self._get_singleton_without_checks(id_)

        if singleton is not None:
            return singleton

        service = self._get_service_without_checks(id_, arguments)

        if service is not None:
            return service

        aliased = self._get_aliased_without_checks(id_, arguments)

        if aliased is not None:
            return aliased

        return self._get_fallback(id_, arguments, mode)

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
        aliased = self._get_alias(id_)

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

        self._instances[id_] = singleton

        return singleton

    def _get_service_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        """Get a service, without an alias step and without a publish step."""
        factory = self._get_service_factory(id_)

        if factory is None:
            return None

        return factory(self, arguments)

    def _get_alias(self, id_: str) -> str | None:
        """Get the id that an alias points to."""
        return self._aliases.get(id_)

    def _get_singleton_instance(self, id_: str) -> object | None:
        """Get the singleton instance that the container holds for an id."""
        return self._instances.get(id_)

    def _get_service_factory(self, id_: str) -> ServiceFactory | None:
        """Get the factory that the container holds for an id."""
        return self._services.get(id_)

    def _get_fallback(self, id_: str, arguments: dict[str, Any], mode: InvalidReferenceMode) -> object:
        """Raise, because the container has no service for the id.

        Warning: the fallback ignores `mode`, and it raises for
        `NEW_INSTANCE_OR_THROW_EXCEPTION` too. An id is a string constant such
        as `io.valkyrja.container.ContainerContract`, and that string names no
        Python module, so the container cannot construct the class that the id
        stands for. PHP and Java construct it, because a PHP id is a class name
        and a Java id is a class object. TypeScript raises for the same reason
        as Python.
        """
        raise ContainerInvalidReferenceException(id_)
