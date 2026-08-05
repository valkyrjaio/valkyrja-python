#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.http.message.param.contract.server_param_collection_contract import ServerParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class ServerParamCollection(ParamCollection, ServerParamCollectionContract):
    """The parameters that server carries."""
