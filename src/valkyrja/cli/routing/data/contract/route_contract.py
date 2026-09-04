#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, Self

from valkyrja.cli.interaction.message.contract.message_contract import MessageContract
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.routing.data.contract.argument_parameter_contract import (
    ArgumentParameterContract,
)
from valkyrja.cli.routing.data.contract.option_parameter_contract import OptionParameterContract
from valkyrja.container.manager.contract.container_contract import ContainerContract

type CliHandler = Callable[[ContainerContract, dict[str, Any]], OutputContract]
"""The router calls this handler when the route matches."""

type HelpText = Callable[[], MessageContract]
"""The route builds its help text only when a reader asks for it."""


class RouteContract(ABC):
    """The contract for one command that the application answers."""

    @abstractmethod
    def get_name(self) -> str:
        """Get the name of the command."""

    @abstractmethod
    def with_name(self, name: str) -> Self:
        """Get a copy of the route that carries a different name."""

    @abstractmethod
    def get_description(self) -> str:
        """Get the description that the help text shows."""

    @abstractmethod
    def with_description(self, description: str) -> Self:
        """Get a copy of the route that carries a different description."""

    @abstractmethod
    def has_help_text(self) -> bool:
        """Get whether the route carries help text."""

    @abstractmethod
    def get_help_text(self) -> HelpText:
        """Get the callable that builds the help text."""

    @abstractmethod
    def get_help_text_message(self) -> MessageContract:
        """Get the help text as a message."""

    @abstractmethod
    def with_help_text(self, help_text: HelpText) -> Self:
        """Get a copy of the route that carries different help text."""

    @abstractmethod
    def has_arguments(self) -> bool:
        """Get whether the command declares an argument."""

    @abstractmethod
    def get_arguments(self) -> list[ArgumentParameterContract]:
        """Get each argument that the command declares."""

    @abstractmethod
    def has_argument(self, name: str) -> bool:
        """Get whether the command declares an argument with a given name."""

    @abstractmethod
    def get_argument(self, name: str) -> ArgumentParameterContract:
        """Get the argument that carries a given name."""

    @abstractmethod
    def has_provided_argument(self, name: str) -> bool:
        """Get whether the invocation gave an argument that the route declares."""

    @abstractmethod
    def get_argument_value(self, name: str, default: str = "") -> str:
        """Get the first value the invocation gave an argument, or the default."""

    @abstractmethod
    def with_arguments(self, *arguments: ArgumentParameterContract) -> Self:
        """Get a copy of the route that declares different arguments."""

    @abstractmethod
    def with_added_arguments(self, *arguments: ArgumentParameterContract) -> Self:
        """Get a copy of the route that declares more arguments."""

    @abstractmethod
    def has_options(self) -> bool:
        """Get whether the command declares an option."""

    @abstractmethod
    def get_options(self) -> list[OptionParameterContract]:
        """Get each option that the command declares."""

    @abstractmethod
    def has_option(self, name: str) -> bool:
        """Get whether the command declares an option with a given name."""

    @abstractmethod
    def get_option(self, name: str) -> OptionParameterContract:
        """Get the option that carries a given name."""

    @abstractmethod
    def has_provided_option(self, name: str) -> bool:
        """Get whether the invocation gave an option that the route declares."""

    @abstractmethod
    def get_option_value(self, name: str, default: str | None = None) -> str:
        """Get the first value the invocation gave an option.

        A default given here wins, and None is the only value that reaches the
        option's own declared default value.
        """

    @abstractmethod
    def with_options(self, *options: OptionParameterContract) -> Self:
        """Get a copy of the route that declares different options."""

    @abstractmethod
    def with_added_options(self, *options: OptionParameterContract) -> Self:
        """Get a copy of the route that declares more options."""

    @abstractmethod
    def get_route_matched_middleware(self) -> list[str]:
        """Get each `RouteMatchedMiddlewareContract` that the route schedules."""

    @abstractmethod
    def with_route_matched_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules different middleware."""

    @abstractmethod
    def with_added_route_matched_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules more middleware.

        Warning: the route appends, and it never dedupes. A middleware that a
        caller adds twice runs twice.
        """

    @abstractmethod
    def get_route_dispatched_middleware(self) -> list[str]:
        """Get each `RouteDispatchedMiddlewareContract` that the route schedules."""

    @abstractmethod
    def with_route_dispatched_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules different middleware."""

    @abstractmethod
    def with_added_route_dispatched_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules more middleware.

        Warning: the route appends, and it never dedupes. A middleware that a
        caller adds twice runs twice.
        """

    @abstractmethod
    def get_throwable_caught_middleware(self) -> list[str]:
        """Get each `ThrowableCaughtMiddlewareContract` that the route schedules."""

    @abstractmethod
    def with_throwable_caught_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules different middleware."""

    @abstractmethod
    def with_added_throwable_caught_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules more middleware.

        Warning: the route appends, and it never dedupes. A middleware that a
        caller adds twice runs twice.
        """

    @abstractmethod
    def get_process_exiting_middleware(self) -> list[str]:
        """Get each `ProcessExitingMiddlewareContract` that the route schedules."""

    @abstractmethod
    def with_process_exiting_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules different middleware."""

    @abstractmethod
    def with_added_process_exiting_middleware(self, *middleware: str) -> Self:
        """Get a copy of the route that schedules more middleware.

        Warning: the route appends, and it never dedupes. A middleware that a
        caller adds twice runs twice.
        """

    @abstractmethod
    def get_handler(self) -> CliHandler:
        """Get the handler that answers the command."""

    @abstractmethod
    def with_handler(self, handler: CliHandler) -> Self:
        """Get a copy of the route that carries a different handler."""
