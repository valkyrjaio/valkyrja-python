#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the outputs."""

from pathlib import Path
from typing import Any

from valkyrja.cli.interaction.enum.exit_code import ExitCode
from valkyrja.cli.interaction.message.message import Message
from valkyrja.cli.interaction.output.empty_output import EmptyOutput
from valkyrja.cli.interaction.output.factory.output_factory import OutputFactory
from valkyrja.cli.interaction.output.file_output import FileOutput
from valkyrja.cli.interaction.output.output import Output
from valkyrja.cli.interaction.output.plain_output import PlainOutput
from valkyrja.cli.interaction.output.stream_output import StreamOutput


def test_a_new_output_has_defaults() -> None:
    output = Output()

    assert output.is_interactive()
    assert not output.is_quiet()
    assert not output.is_silent()
    assert output.get_exit_code() is ExitCode.SUCCESS
    assert output.get_messages() == []
    assert len(output.get_writers()) == 1


def test_an_output_holds_the_messages_it_takes() -> None:
    output = Output(True, False, False, ExitCode.SUCCESS, Message("a"))

    assert output.has_unwritten_message()
    assert not output.has_written_message()
    assert len(output.get_messages()) == 1


def test_with_messages_replaces_the_unwritten_messages() -> None:
    output = Output(True, False, False, ExitCode.SUCCESS, Message("a"))

    changed = output.with_messages(Message("b"))

    assert [m.get_text() for m in changed.get_unwritten_messages()] == ["b"]
    assert [m.get_text() for m in output.get_unwritten_messages()] == ["a"]


def test_with_added_messages_appends() -> None:
    output = Output(True, False, False, ExitCode.SUCCESS, Message("a"))

    changed = output.with_added_messages(Message("b"), Message("c"))

    assert [m.get_text() for m in changed.get_unwritten_messages()] == ["a", "b", "c"]
    assert len(output.get_unwritten_messages()) == 1


def test_with_added_message_appends_one() -> None:
    changed = Output().with_added_message(Message("a"))

    assert [m.get_text() for m in changed.get_unwritten_messages()] == ["a"]


def test_write_messages_moves_each_message_to_written(capsys: Any) -> None:
    output = Output(True, False, False, ExitCode.SUCCESS, Message("a"), Message("b"))

    written = output.write_messages()

    assert capsys.readouterr().out == "ab"
    assert not written.has_unwritten_message()
    assert [m.get_text() for m in written.get_written_messages()] == ["a", "b"]


def test_write_message_records_and_prints(capsys: Any) -> None:
    output = Output()

    output.write_message(Message("a"))

    assert capsys.readouterr().out == "a"
    assert output.has_written_message()


def test_a_silent_output_records_but_prints_nothing(capsys: Any) -> None:
    output = Output(is_silent=True)

    output.write_message(Message("a"))

    assert capsys.readouterr().out == ""
    assert output.has_written_message()


def test_a_quiet_output_prints_nothing_on_success(capsys: Any) -> None:
    output = Output(is_quiet=True)

    output.write_message(Message("a"))

    assert capsys.readouterr().out == ""


def test_a_quiet_output_prints_on_a_failure(capsys: Any) -> None:
    output = Output(is_quiet=True, exit_code=ExitCode.ERROR)

    output.write_message(Message("a"))

    assert capsys.readouterr().out == "a"


def test_get_messages_puts_the_written_messages_first(capsys: Any) -> None:
    output = Output(True, False, False, ExitCode.SUCCESS, Message("unwritten"))
    output.write_message(Message("written"))
    capsys.readouterr()

    assert [m.get_text() for m in output.get_messages()] == ["written", "unwritten"]


def test_with_writers_replaces_them() -> None:
    output = Output()

    assert output.with_writers().get_writers() == []
    assert len(output.get_writers()) == 1


def test_get_writers_copies_the_list() -> None:
    output = Output()

    output.get_writers().clear()

    assert len(output.get_writers()) == 1


def test_the_flags_return_copies() -> None:
    output = Output()

    assert not output.with_is_interactive(False).is_interactive()
    assert output.with_is_quiet(True).is_quiet()
    assert output.with_is_silent(True).is_silent()
    assert output.with_exit_code(ExitCode.ERROR).get_exit_code() is ExitCode.ERROR
    assert output.is_interactive()
    assert output.get_exit_code() is ExitCode.SUCCESS


def test_a_plain_output_removes_a_tag(capsys: Any) -> None:
    output = PlainOutput()

    output.write_message(Message("<b>bold</b> text"))

    assert capsys.readouterr().out == "bold text"


def test_an_empty_output_prints_nothing_and_records(capsys: Any) -> None:
    output = EmptyOutput()

    output.write_message(Message("a"))

    assert capsys.readouterr().out == ""
    assert output.has_written_message()


def test_a_stream_output_writes_to_its_stream(tmp_path: Path) -> None:
    path = tmp_path / "stream.txt"

    with path.open("w", encoding="utf-8") as stream:
        output = StreamOutput(stream)
        output.write_message(Message("a"))

    assert path.read_text(encoding="utf-8") == "a"


def test_with_stream_returns_a_copy(tmp_path: Path) -> None:
    path = tmp_path / "stream.txt"

    with path.open("w", encoding="utf-8") as first, path.open("a", encoding="utf-8") as second:
        output = StreamOutput(first)
        changed = output.with_stream(second)

        assert changed is not output
        assert changed.get_stream() is second
        assert output.get_stream() is first


def test_a_file_output_appends_to_its_file(tmp_path: Path) -> None:
    path = tmp_path / "out.txt"
    output = FileOutput(str(path))

    output.write_message(Message("a"))
    output.write_message(Message("b"))

    assert path.read_text(encoding="utf-8") == "ab"
    assert output.get_filepath() == str(path)


def test_with_filepath_returns_a_copy(tmp_path: Path) -> None:
    output = FileOutput(str(tmp_path / "one.txt"))

    changed = output.with_filepath(str(tmp_path / "two.txt"))

    assert changed is not output
    assert changed.get_filepath().endswith("two.txt")
    assert output.get_filepath().endswith("one.txt")


def test_the_output_factory_builds_each_kind(tmp_path: Path) -> None:
    factory = OutputFactory()

    assert isinstance(factory.create_output(), Output)
    assert isinstance(factory.create_empty_output(), EmptyOutput)
    assert isinstance(factory.create_plain_output(), PlainOutput)
    assert isinstance(factory.create_file_output(str(tmp_path / "f.txt")), FileOutput)
    assert isinstance(factory.create_stream_output(), StreamOutput)


def test_the_output_factory_passes_the_exit_code_and_messages() -> None:
    output = OutputFactory().create_output(Message("a"), exit_code=ExitCode.ERROR)

    assert output.get_exit_code() is ExitCode.ERROR
    assert len(output.get_messages()) == 1
