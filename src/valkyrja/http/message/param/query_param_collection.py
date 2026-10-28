#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final, override

from valkyrja.http.message.param.contract.query_param_collection_contract import QueryParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class QueryParamCollection(ParamCollection, QueryParamCollectionContract):
    @override
    def get(self, key: str | int) -> str | QueryParamCollectionContract:
        value: str | QueryParamCollectionContract = super().get(key)

        return value

    @override
    def _is_valid_param(self, value: Any) -> bool:
        """Get whether the collection carries one parameter.

        A query holds text or another query, which is what `get` declares.
        """
        return isinstance(value, (str, type(self)))

    @override
    @classmethod
    def _get_default(cls) -> str | QueryParamCollectionContract:
        return ""
