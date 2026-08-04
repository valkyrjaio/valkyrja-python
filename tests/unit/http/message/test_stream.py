#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the Stream."""

import sys
from pathlib import Path

import pytest

from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream
from valkyrja.http.message.stream.factory.stream_factory import StreamFactory
from valkyrja.http.message.stream.stream import Stream
from valkyrja.http.message.stream.throwable.exception.http_stream_exception import (
    HttpStreamException,
)


def make_stream(text: str = "") -> Stream:
    stream = Stream()

    if text:
        stream.write(text)
        stream.rewind()

    return stream


def test_a_new_stream_is_empty() -> None:
    assert make_stream().get_size() == 0


def test_write_returns_the_number_of_characters() -> None:
    assert make_stream().write("hello") == 5


def test_a_stream_reads_what_it_wrote() -> None:
    assert make_stream("hello").get_contents() == "hello"


def test_read_takes_a_number_of_characters() -> None:
    assert make_stream("hello").read(2) == "he"


def test_str_reads_the_whole_stream_from_the_start() -> None:
    stream = make_stream("hello")

    stream.read(2)

    assert str(stream) == "hello"


def test_tell_reports_the_place() -> None:
    stream = make_stream("hello")

    stream.read(2)

    assert stream.tell() == 2


def test_seek_moves_the_place() -> None:
    stream = make_stream("hello")

    stream.seek(3)

    assert stream.get_contents() == "lo"


def test_eof_reports_the_end() -> None:
    stream = make_stream("hi")

    assert not stream.eof()

    stream.get_contents()

    assert stream.eof()


def test_get_size_keeps_the_place() -> None:
    stream = make_stream("hello")

    stream.read(2)

    assert stream.get_size() == 5
    assert stream.tell() == 2


def test_a_stream_in_memory_is_seekable_readable_and_writable() -> None:
    stream = make_stream()

    assert stream.is_seekable()
    assert stream.is_readable()
    assert stream.is_writable()


def test_close_leaves_no_stream() -> None:
    stream = make_stream("hi")

    stream.close()

    assert not stream.is_readable()
    assert not stream.is_writable()
    assert not stream.is_seekable()
    assert stream.eof()
    assert str(stream) == ""
    assert stream.get_metadata() == {}
    assert stream.get_metadata_item("mode") is None


def test_detach_gives_the_stream_away() -> None:
    stream = make_stream("hi")

    detached = stream.detach()

    assert detached is not None
    assert stream.detach() is None
    assert not stream.is_readable()


@pytest.mark.parametrize(
    "call",
    [
        lambda stream: stream.read(1),
        lambda stream: stream.get_contents(),
        lambda stream: stream.write("x"),
        lambda stream: stream.seek(0),
        lambda stream: stream.tell(),
    ],
)
def test_a_detached_stream_reports_a_failure(call: object) -> None:
    stream = make_stream("hi")
    stream.detach()

    with pytest.raises(HttpStreamException):
        call(stream)  # type: ignore[operator]


def test_the_metadata_describes_the_stream() -> None:
    metadata = make_stream("hi").get_metadata()

    assert metadata["seekable"]
    assert metadata["readable"]
    assert metadata["writable"]
    assert make_stream("hi").get_metadata_item("readable")


def test_the_factory_answers_with_each_standard_stream() -> None:
    assert StreamFactory.get_resource_stream(StandardStream.STDIN) is sys.stdin
    assert StreamFactory.get_resource_stream(StandardStream.STDOUT) is sys.stdout
    assert StreamFactory.get_resource_stream(StandardStream.STDERR) is sys.stderr


def test_the_factory_opens_a_file(tmp_path: Path) -> None:
    path = tmp_path / "body.txt"
    path.write_text("from a file", encoding="utf-8")

    stream = Stream(str(path), Mode.READ)

    assert stream.get_contents() == "from a file"

    stream.close()


def test_the_modes_that_a_stream_opens_in() -> None:
    assert Mode.READ.value == "r"
    assert Mode.WRITE_READ.value == "w+"
    assert len({mode.value for mode in Mode}) == len(Mode)


def test_close_twice_is_safe() -> None:
    stream = make_stream("hi")

    stream.close()
    stream.close()

    assert not stream.is_readable()


def test_a_memory_stream_in_read_mode_reports_itself_read_only() -> None:
    """`Mode.READ` names a stream a caller reads, so it reports no write."""
    stream = Stream(mode=Mode.READ)

    assert stream.is_readable()
    assert not stream.is_writable()


def test_an_empty_response_body_takes_no_write() -> None:
    from valkyrja.http.message.response.empty_response import EmptyResponse

    assert not EmptyResponse().get_body().is_writable()
