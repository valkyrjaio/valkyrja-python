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


class ChildContainer(Container):
    """A container that reads a parent container through the contract.

    The child holds its own singleton bindings and its own publishers. The child
    reads the parent for anything that the child does not hold.
    """

    def __init__(self, parent: ContainerContract, data: ContainerData) -> None:
        super().__init__()

        self._parent = parent
        self._singletons = dict(data.singletons)
        self._callbacks.update(data.callbacks)

    @override
    def is_alias(self, id_: str) -> bool:
        return super().is_alias(id_) or self._parent.is_alias(id_)

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
        """Get a singleton, in this order.

        1. The instance that the child resolved already.
        2. The instance that the parent resolved already, because a resolved
           instance is safe to share.
        3. A new instance from the binding of the child, which keeps the child
           apart from the parent.
        """
        if not super().is_singleton_instance(id_) and self._parent.is_singleton_instance(id_):
            return self._parent.get_singleton(id_)

        return super()._get_singleton_without_checks(id_)

    @override
    def _get_service_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        if not super().is_service(id_) and self._parent.is_service(id_):
            return self._parent.get_service(id_, arguments)

        return super()._get_service_without_checks(id_, arguments)

    @override
    def _get_aliased_without_checks(self, id_: str, arguments: dict[str, Any]) -> object | None:
        if not super().is_alias(id_) and self._parent.is_alias(id_):
            return self._parent.get_aliased(id_, arguments)

        return super()._get_aliased_without_checks(id_, arguments)
