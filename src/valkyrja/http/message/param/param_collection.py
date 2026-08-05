#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from copy import copy
from typing import Any, Self, override

from valkyrja.http.message.param.contract.param_collection_contract import ParamCollectionContract


class ParamCollection(ParamCollectionContract):
    """A collection of parameters that a request carries."""

    def __init__(self, params: dict[str | int, Any] | None = None) -> None:
        self._params: dict[str | int, Any] = dict(params) if params is not None else {}

    @override
    def has(self, key: str | int) -> bool:
        return key in self._params

    @override
    def get(self, key: str | int) -> Any:
        return self._params.get(key)

    @override
    def get_all(self) -> dict[str | int, Any]:
        return dict(self._params)

    @override
    def get_only(self, *keys: str | int) -> dict[str | int, Any]:
        return {key: value for key, value in self._params.items() if key in keys}

    @override
    def get_all_except(self, *keys: str | int) -> dict[str | int, Any]:
        return {key: value for key, value in self._params.items() if key not in keys}

    @override
    def with_(self, params: dict[str | int, Any]) -> Self:
        new = copy(self)
        new._params = dict(params)

        return new

    @override
    def with_added(self, params: dict[str | int, Any]) -> Self:
        new = copy(self)
        new._params = {**self._params, **params}

        return new
