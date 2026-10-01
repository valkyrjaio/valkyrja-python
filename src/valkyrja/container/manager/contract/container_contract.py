#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Any, Self

from valkyrja.container.data.container_data import ContainerData, ServiceFactory
from valkyrja.container.manager.contract.providers_aware_contract import ProvidersAwareContract


class ContainerContract(ProvidersAwareContract):
    @abstractmethod
    def get_data(self) -> ContainerData:
        """Get a data representation of the container."""

    @abstractmethod
    def set_from_data(self, data: ContainerData) -> None:
        """Add the state of a data object to the container."""

    @abstractmethod
    def has(self, id_: str) -> bool:
        """Get whether the container has a service for a given id."""

    @abstractmethod
    def bind(self, id_: str, factory: ServiceFactory) -> Self:
        """Bind a service to the container.

        The container calls the factory each time an application asks for the id.
        """

    @abstractmethod
    def bind_alias(self, alias: str, id_: str) -> Self:
        """Bind an alias to a service id."""

    @abstractmethod
    def bind_singleton(self, id_: str, factory: ServiceFactory) -> Self:
        """Bind a singleton to the container.

        The container calls the factory once, then it keeps the result.
        """

    @abstractmethod
    def set_singleton(self, id_: str, singleton: object) -> Self:
        """Set a singleton instance in the container."""

    @abstractmethod
    def is_alias(self, id_: str) -> bool:
        """Get whether a given id is an alias."""

    @abstractmethod
    def get_aliased_id(self, alias: str) -> str | None:
        """Get the id that a given alias points to, or None when it is no alias."""

    @abstractmethod
    def is_service(self, id_: str) -> bool:
        """Get whether a given id is a service."""

    @abstractmethod
    def is_singleton(self, id_: str) -> bool:
        """Get whether a given id is a singleton."""

    @abstractmethod
    def is_singleton_binding(self, id_: str) -> bool:
        """Get whether a given id has a singleton binding that is not resolved yet."""

    @abstractmethod
    def is_singleton_instance(self, id_: str) -> bool:
        """Get whether a given id has a singleton instance already."""

    @abstractmethod
    def get(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        """Get a service from the container.

        The container looks for a singleton, then a service, then an alias, and it
        raises when it finds none of them.
        """

    @abstractmethod
    def get_aliased(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        """Get the service that a given alias points to."""

    @abstractmethod
    def get_service(self, id_: str, arguments: dict[str, Any] | None = None) -> object:
        """Get a service from the container."""

    @abstractmethod
    def get_singleton(self, id_: str) -> object:
        """Get a singleton from the container."""
