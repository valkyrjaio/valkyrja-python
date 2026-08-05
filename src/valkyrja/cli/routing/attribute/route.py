#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, TypeVar

from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.cli.routing.data.contract.route_contract import HelpText

Function = TypeVar("Function", bound=Callable[..., Any])
"""The decorator returns the function it received, with its type intact."""

ROUTE_MARKER = "_valkyrja_cli_route"
"""The attribute that `@route` attaches to a function."""


@dataclass(frozen=True)
class RouteMarker:
    """What `@route` records about one command.

    PHP writes `#[Route(...)]` above the method. Python has no attribute, so the
    decorator attaches this marker to the function instead.
    """

    name: str
    description: str
    help_text: HelpText | None = None
    route_matched_middleware: list[str] = field(default_factory=list)
    route_dispatched_middleware: list[str] = field(default_factory=list)
    throwable_caught_middleware: list[str] = field(default_factory=list)
    process_exiting_middleware: list[str] = field(default_factory=list)
    arguments: list[ArgumentParameterContract] = field(default_factory=list)
    options: list[OptionParameterContract] = field(default_factory=list)


def route(
    name: str,
    description: str,
    help_text: HelpText | None = None,
    route_matched_middleware: list[str] | None = None,
    route_dispatched_middleware: list[str] | None = None,
    throwable_caught_middleware: list[str] | None = None,
    process_exiting_middleware: list[str] | None = None,
    arguments: list[ArgumentParameterContract] | None = None,
    options: list[OptionParameterContract] | None = None,
) -> Callable[[Function], Function]:
    """Mark a function as the handler of one command.

    Warning: the decorator records metadata and nothing else. It never registers
    the command. The collector reads the marker at bootstrap, and `sindri` reads
    it from the source, so a cached application never runs the collector.
    """

    def decorator(function: Function) -> Function:
        setattr(
            function,
            ROUTE_MARKER,
            RouteMarker(
                name=name,
                description=description,
                help_text=help_text,
                route_matched_middleware=list(route_matched_middleware or []),
                route_dispatched_middleware=list(route_dispatched_middleware or []),
                throwable_caught_middleware=list(throwable_caught_middleware or []),
                process_exiting_middleware=list(process_exiting_middleware or []),
                arguments=list(arguments or []),
                options=list(options or []),
            ),
        )

        return function

    return decorator
