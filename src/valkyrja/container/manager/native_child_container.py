#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import override

from valkyrja.container.data.container_data import PublishCallback, ServiceFactory
from valkyrja.container.manager.container import Container


class NativeChildContainer(Container):
    """A container that reads the state of a parent `Container` directly.

    The child reads each map of the parent, so a lookup costs one dictionary
    read and never a call through the contract. `ChildContainer` reads the
    parent through the contract instead, and it accepts any container.

    The class reads a protected member of the parent, the same as PHP. The
    parent is a `Container`, not a `ContainerContract`, and that narrower type
    is what makes the direct read valid.
    """

    def __init__(self, parent: Container) -> None:
        super().__init__()

        self._parent = parent

    @override
    def is_alias(self, id_: str) -> bool:
        return self._get_alias(id_) is not None

    @override
    def is_service(self, id_: str) -> bool:
        return self._get_service_factory(id_) is not None

    @override
    def is_singleton_binding(self, id_: str) -> bool:
        return id_ in self._singletons or id_ in self._parent._singletons

    @override
    def is_singleton_instance(self, id_: str) -> bool:
        return id_ in self._instances or id_ in self._parent._instances

    @override
    def has(self, id_: str) -> bool:
        return (
            id_ in self._callbacks
            or id_ in self._parent._callbacks
            or self.is_singleton(id_)
            or self.is_service(id_)
            or self.is_alias(id_)
        )

    @override
    def is_published(self, id_: str) -> bool:
        return id_ in self._published or id_ in self._parent._published

    @override
    def _publish_unpublished_provided(self, id_: str) -> None:
        if (id_ in self._callbacks or id_ in self._parent._callbacks) and not self.is_published(id_):
            self.publish(id_)

    # Warning: each lookup below tests for `None`, never for a false value. PHP
    # chains these with `??`, which tests for null alone. An empty alias string
    # is a false value, so `or` would read past it to the parent.
    @override
    def _get_callback(self, id_: str) -> PublishCallback | None:
        callback = self._callbacks.get(id_)

        return callback if callback is not None else self._parent._callbacks.get(id_)

    @override
    def _get_alias(self, id_: str) -> str | None:
        alias = self._aliases.get(id_)

        return alias if alias is not None else self._parent._aliases.get(id_)

    @override
    def _get_singleton_instance(self, id_: str) -> object | None:
        instance = self._instances.get(id_)

        return instance if instance is not None else self._parent._instances.get(id_)

    @override
    def _get_service_factory(self, id_: str) -> ServiceFactory | None:
        factory = self._services.get(id_)

        return factory if factory is not None else self._parent._services.get(id_)
