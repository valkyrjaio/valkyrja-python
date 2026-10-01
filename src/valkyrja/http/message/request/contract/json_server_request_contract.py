#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import abstractmethod
from typing import Self

from valkyrja.http.message.param.contract.parsed_json_param_collection_contract import (
    ParsedJsonParamCollectionContract,
)
from valkyrja.http.message.request.contract.server_request_contract import ServerRequestContract


class JsonServerRequestContract(ServerRequestContract):
    @abstractmethod
    def get_parsed_json(self) -> ParsedJsonParamCollectionContract:
        """Get the json that the body of the request holds."""

    @abstractmethod
    def with_parsed_json(self, params: ParsedJsonParamCollectionContract) -> Self:
        """Get a copy of the request that carries different json."""
