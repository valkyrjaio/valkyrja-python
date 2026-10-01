#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final, override

from valkyrja.http.message.param.contract.server_param_collection_contract import ServerParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class ServerParamCollection(ParamCollection, ServerParamCollectionContract):
    @override
    def get(self, key: str | int) -> str | int | float | bool | ServerParamCollectionContract:
        value: str | int | float | bool | ServerParamCollectionContract = super().get(key)

        return value

    @override
    @classmethod
    def _get_default(cls) -> str | int | float | bool | ServerParamCollectionContract:
        return ""
