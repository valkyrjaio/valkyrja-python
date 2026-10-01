#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

from difflib import SequenceMatcher
from typing import override

from valkyrja.cli.interaction.input.contract.input_contract import InputContract
from valkyrja.cli.interaction.message.answer import Answer
from valkyrja.cli.interaction.message.contract.answer_contract import AnswerContract
from valkyrja.cli.interaction.message.new_line import NewLine
from valkyrja.cli.interaction.message.question import Question
from valkyrja.cli.interaction.output.contract.output_contract import OutputContract
from valkyrja.cli.middleware.contract.route_not_matched_middleware_contract import (
    RouteNotMatchedMiddlewareContract,
)
from valkyrja.cli.middleware.handler.contract.route_not_matched_handler_contract import (
    RouteNotMatchedHandlerContract,
)
from valkyrja.cli.routing.collection.contract.route_collection_contract import (
    RouteCollectionContract,
)
from valkyrja.cli.routing.data.contract.route_contract import RouteContract
from valkyrja.cli.routing.dispatcher.contract.router_contract import RouterContract

SIMILARITY_THRESHOLD = 60.0
"""The percentage two names share before the middleware offers one of them."""

DECLINED_RESPONSE = "no"
"""The response that runs no command."""


class CheckCommandForTypoMiddleware(RouteNotMatchedMiddlewareContract):
    def __init__(
        self,
        router: RouterContract,
        collection: RouteCollectionContract,
        default_answer: str = DECLINED_RESPONSE,
    ) -> None:
        self._router = router
        self._collection = collection
        self._default_answer = default_answer
        self._matched_route: RouteContract | None = None

    @override
    def route_not_matched(
        self, input_: InputContract, output: OutputContract, handler: RouteNotMatchedHandlerContract
    ) -> OutputContract:
        route_or_output = self._check_command_name_for_typo(input_, output)

        if isinstance(route_or_output, RouteContract):
            output = self._router.dispatch(input_.with_command_name(route_or_output.get_name()))
        else:
            output = route_or_output

        return handler.route_not_matched(input_, output)

    def _check_command_name_for_typo(
        self, input_: InputContract, output: OutputContract
    ) -> RouteContract | OutputContract:
        """Get a command whose name is close to the one the input names."""
        name = input_.get_command_name()
        commands = [
            command
            for command in self._collection.all().values()
            if self._get_similarity(command.get_name(), name) >= SIMILARITY_THRESHOLD
        ]

        if commands:
            return self._ask_to_run_similar_commands(output, commands)

        return output

    def _ask_to_run_similar_commands(
        self, output: OutputContract, commands: list[RouteContract]
    ) -> RouteContract | OutputContract:
        """Offer each close command, and read the one that the user names."""
        command_names = [command.get_name() for command in commands]

        def callback(answered_output: OutputContract, answer: AnswerContract) -> OutputContract:
            return self._question_callback(answered_output, answer, commands)

        output = output.with_added_messages(
            NewLine(),
            Question(
                "Did you mean to run one of the following commands?",
                callback,
                Answer(default_response=self._default_answer, allowed_responses=command_names),
            ),
        ).write_messages()

        return self._matched_route if self._matched_route is not None else output

    def _question_callback(
        self, output: OutputContract, answer: AnswerContract, commands: list[RouteContract]
    ) -> OutputContract:
        """Keep the command that the response names, so the stage dispatches it."""
        response = answer.get_user_response()
        self._matched_route = self._get_matched_route(commands, response) if response != DECLINED_RESPONSE else None

        return output

    @staticmethod
    def _get_matched_route(commands: list[RouteContract], response: str) -> RouteContract | None:
        """Get the command whose name the response names."""
        return next((command for command in commands if command.get_name() == response), None)

    @staticmethod
    def _get_similarity(first: str, second: str) -> float:
        """Get how much two names share, as a percentage.

        PHP reads this from `similar_text`, which reports the same ratio of shared
        characters to the combined length that `SequenceMatcher` reports.
        """
        return SequenceMatcher(None, first, second).ratio() * 100
