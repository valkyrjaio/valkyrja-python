#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final, override

from valkyrja.http.message.param.contract.parsed_body_param_collection_contract import ParsedBodyParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class ParsedBodyParamCollection(ParamCollection, ParsedBodyParamCollectionContract):
    @override
    def get(self, key: str | int) -> str | ParsedBodyParamCollectionContract:
        value: str | ParsedBodyParamCollectionContract = super().get(key)

        return value

    @override
    def _is_valid_param(self, value: Any) -> bool:
        """Get whether the collection carries one parameter.

        A parsed body holds text or another body, which is what `get` declares.
        """
        return isinstance(value, (str, type(self)))

    @override
    @classmethod
    def _get_default(cls) -> str | ParsedBodyParamCollectionContract:
        return ""
