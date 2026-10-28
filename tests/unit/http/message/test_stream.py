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

from tests.fixtures.http.message.failing_stream_fixture import (
    FailingStreamFixture,
    UnseekableStreamFixture,
)
from valkyrja.http.message.stream.enum.mode import Mode
from valkyrja.http.message.stream.enum.standard_stream import StandardStream
from valkyrja.http.message.stream.factory.stream_factory import StreamFactory
from valkyrja.http.message.stream.stream import Stream
from valkyrja.http.message.stream.throwable.contract.http_stream_throwable import (
    HttpStreamThrowable,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_length_exception import (
    HttpStreamInvalidLengthException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_invalid_stream_exception import (
    HttpStreamInvalidStreamException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_read_exception import (
    HttpStreamStreamReadException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_seek_exception import (
    HttpStreamStreamSeekException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_tell_exception import (
    HttpStreamStreamTellException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_stream_write_exception import (
    HttpStreamStreamWriteException,
)
from valkyrja.http.message.stream.throwable.exception.http_stream_unwritable_stream_exception import (
    HttpStreamUnwritableStreamException,
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
    assert make_stream("hello").get_contents() == b"hello"


def test_read_takes_a_number_of_characters() -> None:
    assert make_stream("hello").read(2) == b"he"


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

    assert stream.get_contents() == b"lo"


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

    # Each call names its own failure, and every one of them is a stream throwable.
    with pytest.raises(HttpStreamThrowable):
        call(stream)  # type: ignore[operator]


def test_the_metadata_describes_the_stream() -> None:
    metadata = make_stream("hi").get_metadata()

    assert metadata["seekable"]
    assert metadata["readable"]
    assert metadata["writable"]
    assert make_stream("hi").get_metadata_item("readable")


def test_the_factory_answers_with_the_byte_buffer_of_each_standard_stream() -> None:
    # A body is bytes, so the factory answers with the buffer under the text stream.
    assert StreamFactory.get_resource_stream(StandardStream.STDIN) is sys.stdin.buffer
    assert StreamFactory.get_resource_stream(StandardStream.STDOUT) is sys.stdout.buffer
    assert StreamFactory.get_resource_stream(StandardStream.STDERR) is sys.stderr.buffer


def test_the_factory_opens_a_file(tmp_path: Path) -> None:
    path = tmp_path / "body.txt"
    path.write_text("from a file", encoding="utf-8")

    stream = Stream(str(path), Mode.READ)

    assert stream.get_contents() == b"from a file"

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


def test_closing_a_standard_stream_leaves_the_process_stream_open() -> None:
    # The process owns this stream, so closing it would take it from every reader.
    stream = Stream(StandardStream.STDOUT)

    stream.close()

    assert not sys.stdout.buffer.closed
    assert sys.stdout.buffer is not None


def test_closing_a_stream_in_memory_closes_it() -> None:
    stream = make_stream("hi")
    detached = stream.detach()

    assert detached is not None
    assert not detached.closed

    stream = make_stream("hi")
    stream.close()

    assert stream.get_metadata() == {}


def test_a_create_mode_opens_a_file_that_is_absent(tmp_path: Path) -> None:
    path = tmp_path / "new.txt"

    stream = Stream(str(path), Mode.WRITE_READ_CREATE)
    stream.write(b"created")
    # The handle buffers the write, so the close is what puts it on the disk.
    stream.close()

    assert path.read_bytes() == b"created"


def test_a_create_mode_keeps_what_a_file_already_holds(tmp_path: Path) -> None:
    path = tmp_path / "kept.txt"
    path.write_bytes(b"kept")

    stream = Stream(str(path), Mode.WRITE_CREATE)

    assert stream.get_size() == 4


def test_a_create_mode_reads_a_file_from_the_start(tmp_path: Path) -> None:
    path = tmp_path / "start.txt"
    path.write_bytes(b"abc")

    stream = Stream(str(path), Mode.WRITE_READ_CREATE)

    assert stream.get_contents() == b"abc"


def test_read_refuses_a_negative_length() -> None:
    with pytest.raises(HttpStreamInvalidLengthException, match="must not be negative"):
        make_stream("hi").read(-1)


def test_the_factory_reports_a_file_it_cannot_open(tmp_path: Path) -> None:
    with pytest.raises(HttpStreamInvalidStreamException, match="Unable to open the stream"):
        Stream(str(tmp_path / "missing" / "body.txt"))


def test_write_takes_bytes_and_a_string() -> None:
    stream = Stream()

    assert stream.write(b"a") == 1
    assert stream.write("b") == 1

    stream.rewind()

    assert stream.get_contents() == b"ab"


def test_an_unwritable_stream_refuses_a_write() -> None:
    with pytest.raises(HttpStreamUnwritableStreamException, match="not writable"):
        Stream(StandardStream.MEMORY, Mode.READ).write(b"a")


def test_the_size_of_a_stream_that_cannot_seek() -> None:
    stream = Stream()
    detached = stream.detach()

    assert detached is not None


def make_failing_stream() -> Stream:
    """Build a stream over a device that refuses every operation.

    The guards that report a failed device need a device that fails, and no real
    stream of the component does that.
    """
    stream = Stream()
    stream._stream = FailingStreamFixture()

    return stream


def test_the_size_of_a_stream_that_cannot_seek_reads_as_zero() -> None:
    stream = Stream()
    stream._stream = UnseekableStreamFixture()

    assert stream.get_size() == 0


def test_tell_reports_a_device_that_lost_the_position() -> None:
    with pytest.raises(HttpStreamStreamTellException, match="position of the stream"):
        make_failing_stream().tell()


def test_seek_reports_a_device_that_refused_the_seek() -> None:
    with pytest.raises(HttpStreamStreamSeekException, match="Unable to seek"):
        make_failing_stream().seek(1)


def test_write_reports_a_device_that_refused_the_write() -> None:
    with pytest.raises(HttpStreamStreamWriteException, match="Unable to write"):
        make_failing_stream().write(b"a")


def test_read_reports_a_device_that_refused_the_read() -> None:
    with pytest.raises(HttpStreamStreamReadException, match="Unable to read"):
        make_failing_stream().read(1)


def test_get_contents_reports_a_device_that_refused_the_read() -> None:
    with pytest.raises(HttpStreamStreamReadException, match="Unable to read"):
        make_failing_stream().get_contents()
