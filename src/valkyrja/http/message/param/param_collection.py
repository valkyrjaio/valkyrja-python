#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy, deepcopy
from typing import Any, Self, override

from valkyrja.http.message.param.contract.param_collection_contract import ParamCollectionContract
from valkyrja.http.message.param.throwable.exception.http_param_invalid_param_exception import (
    HttpParamInvalidParamException,
)

SCALAR_TYPES = (str, int, float, bool)
"""Each type that one parameter holds, beside a nested collection and `None`."""


class ParamCollection(ParamCollectionContract):
    def __init__(self, params: dict[str | int, Any] | None = None) -> None:
        params = params if params is not None else {}

        self._validate_params(params)

        self._params: dict[str | int, Any] = dict(params)

    @classmethod
    def from_array(cls, data: dict[str | int, Any] | list[Any]) -> Self:
        """Build a collection, and build one for each value that holds more values."""
        items: Any = data.items() if isinstance(data, dict) else enumerate(data)
        params: dict[str | int, Any] = {}

        for name, param in items:
            params[name] = cls.from_array(param) if isinstance(param, (dict, list)) else param

        return cls(params)

    @override
    def has(self, key: str | int) -> bool:
        return key in self._params

    @override
    def get(self, key: str | int) -> Any:
        return self._get_copied(self._params.get(key, self._get_default()))

    @override
    def get_all(self) -> dict[str | int, Any]:
        return {key: self._get_copied(value) for key, value in self._params.items()}

    @override
    def get_only(self, *keys: str | int) -> dict[str | int, Any]:
        return {key: self._get_copied(value) for key, value in self._params.items() if key in keys}

    @override
    def get_all_except(self, *keys: str | int) -> dict[str | int, Any]:
        return {key: self._get_copied(value) for key, value in self._params.items() if key not in keys}

    @override
    def with_(self, params: dict[str | int, Any]) -> Self:
        self._validate_params(params)

        new = copy(self)
        new._params = dict(params)

        return new

    @override
    def with_added(self, params: dict[str | int, Any]) -> Self:
        self._validate_params(params)

        new = copy(self)
        new._params = {**self._params, **params}

        return new

    @classmethod
    def _get_default(cls) -> Any:
        """Get what the collection answers for a key it does not hold."""
        return None

    @staticmethod
    def _get_copied(value: Any) -> Any:
        """Get a copy of the value, so a caller changes no parameter of the collection.

        A nested collection holds its own parameters, and a caller that reads one
        would otherwise change what the request carries.
        """
        return deepcopy(value) if isinstance(value, ParamCollectionContract) else value

    def _validate_params(self, params: dict[str | int, Any]) -> None:
        """Refuse a map that holds a parameter the collection cannot carry."""
        for value in params.values():
            self._validate_param(value)

    def _validate_param(self, value: Any) -> None:
        """Refuse one parameter that the collection cannot carry."""
        if not self._is_valid_param(value):
            raise HttpParamInvalidParamException("Param must be scalar, None, or a collection of the same kind")

    def _is_valid_param(self, value: Any) -> bool:
        """Get whether the collection carries one parameter."""
        return value is None or isinstance(value, (*SCALAR_TYPES, type(self)))
