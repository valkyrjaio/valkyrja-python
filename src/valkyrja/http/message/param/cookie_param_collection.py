#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import Any, final, override

from valkyrja.http.message.param.contract.cookie_param_collection_contract import CookieParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class CookieParamCollection(ParamCollection, CookieParamCollectionContract):
    @override
    def get(self, key: str | int) -> str:
        value: str = super().get(key)

        return value

    @override
    def _is_valid_param(self, value: Any) -> bool:
        """Get whether the collection carries one parameter.

        A cookie value is text, which is what `get` declares.
        """
        return isinstance(value, str)

    @override
    @classmethod
    def _get_default(cls) -> str:
        return ""
