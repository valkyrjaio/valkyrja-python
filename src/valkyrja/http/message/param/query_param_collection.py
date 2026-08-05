#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.http.message.param.contract.query_param_collection_contract import QueryParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class QueryParamCollection(ParamCollection, QueryParamCollectionContract):
    """The parameters that query carries."""
