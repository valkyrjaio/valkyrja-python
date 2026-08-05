#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from typing import final

from valkyrja.http.message.param.contract.cookie_param_collection_contract import CookieParamCollectionContract
from valkyrja.http.message.param.param_collection import ParamCollection


@final
class CookieParamCollection(ParamCollection, CookieParamCollectionContract):
    """The parameters that cookie carries."""
