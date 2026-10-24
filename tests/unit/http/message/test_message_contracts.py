#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the contracts of the Http Message subcomponent.

The implementation pass fills each contract in. Each test pins that the contract
is abstract, so a later change cannot make it constructible without a failure.
"""

import inspect

import pytest

from valkyrja.http.message.contract.message_contract import MessageContract
from valkyrja.http.message.header.collection.contract.header_collection_contract import (
    HeaderCollectionContract,
)
from valkyrja.http.message.header.contract.header_contract import HeaderContract
from valkyrja.http.message.header.value.component.contract.component_contract import (
    ComponentContract,
)
from valkyrja.http.message.header.value.contract.cookie_contract import CookieContract
from valkyrja.http.message.header.value.contract.value_contract import ValueContract
from valkyrja.http.message.request.contract.request_contract import RequestContract
from valkyrja.http.message.response.contract.response_contract import ResponseContract
from valkyrja.http.message.stream.contract.stream_contract import SEEK_SET, StreamContract
from valkyrja.http.message.uri.contract.uri_contract import UriContract
from valkyrja.http.message.uri.enum.scheme import Scheme

CONTRACTS: list[type] = [
    MessageContract,
    RequestContract,
    ResponseContract,
    StreamContract,
    UriContract,
    HeaderContract,
    HeaderCollectionContract,
    ValueContract,
    CookieContract,
    ComponentContract,
]


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_does_not_construct(contract: type) -> None:
    with pytest.raises(TypeError, match="abstract"):
        contract()


@pytest.mark.parametrize("contract", CONTRACTS)
def test_the_contract_declares_an_abstract_method(contract: type) -> None:
    assert inspect.isabstract(contract)


@pytest.mark.parametrize("contract", [RequestContract, ResponseContract])
def test_a_message_contract_extends_the_message_contract(contract: type) -> None:
    assert issubclass(contract, MessageContract)


def test_a_cookie_is_a_header_value() -> None:
    assert issubclass(CookieContract, ValueContract)


def test_the_schemes() -> None:
    assert [scheme.value for scheme in Scheme] == ["", "http", "https"]


def test_seek_set_is_the_start_of_the_stream() -> None:
    assert SEEK_SET == 0
