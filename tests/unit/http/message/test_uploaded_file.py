#
# This file is part of the Valkyrja Framework package.
#
# Copyright (c) 2016-present Melech Mizrachi
#
# Released under the MIT License. See LICENSE.md for details.
#

"""Tests for the uploaded file, its collection, and the json server request."""

from copy import copy
from pathlib import Path
from pickle import dumps, loads

import pytest

from tests.fixtures.http.message.uploaded_file_fixture import FilelessUploadFixture
from valkyrja.http.message.constant.content_type_value import ContentTypeValue
from valkyrja.http.message.constant.header_name import HeaderName
from valkyrja.http.message.file.collection.uploaded_file_collection import UploadedFileCollection
from valkyrja.http.message.file.enum.upload_error import UploadError
from valkyrja.http.message.file.throwable.exception.uploaded_file_already_moved_exception import (
    UploadedFileAlreadyMovedException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_directory_exception import (
    UploadedFileInvalidDirectoryException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_key_exception import (
    UploadedFileInvalidKeyException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_invalid_uploaded_file_exception import (
    UploadedFileInvalidUploadedFileException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_unable_to_write_file_exception import (
    UploadedFileUnableToWriteFileException,
)
from valkyrja.http.message.file.throwable.exception.uploaded_file_upload_error_exception import (
    UploadedFileUploadErrorException,
)
from valkyrja.http.message.file.uploaded_file import UploadedFile
from valkyrja.http.message.header.collection.header_collection import HeaderCollection
from valkyrja.http.message.header.header import Header
from valkyrja.http.message.param.parsed_json_param_collection import ParsedJsonParamCollection
from valkyrja.http.message.param.query_param_collection import QueryParamCollection
from valkyrja.http.message.param.throwable.exception.http_param_invalid_param_exception import (
    HttpParamInvalidParamException,
)
from valkyrja.http.message.request.json_server_request import JsonServerRequest
from valkyrja.http.message.request.server_request import ServerRequest
from valkyrja.http.message.request.throwable.exception.http_request_invalid_json_exception import (
    HttpRequestInvalidJsonException,
)
from valkyrja.http.message.stream.stream import Stream


def make_stream(text: str) -> Stream:
    stream = Stream()
    stream.write(text)
    stream.rewind()

    return stream


def test_an_upload_needs_a_file_or_a_stream() -> None:
    with pytest.raises(UploadedFileInvalidUploadedFileException, match="One of file or stream"):
        UploadedFile()


def test_an_upload_that_reports_a_failure_needs_neither() -> None:
    assert UploadedFile(upload_error=UploadError.NO_FILE).get_error() is UploadError.NO_FILE


def test_an_upload_answers_what_the_client_gave() -> None:
    upload = UploadedFile(stream=make_stream("a"), size=1, file_name="a.txt", media_type="text/plain")

    assert upload.has_size()
    assert upload.get_size() == 1
    assert upload.has_client_filename()
    assert upload.get_client_filename() == "a.txt"
    assert upload.has_client_media_type()
    assert upload.get_client_media_type() == "text/plain"


def test_an_upload_that_names_nothing_reports_so() -> None:
    upload = UploadedFile(stream=make_stream("a"))

    assert not upload.has_size()
    assert not upload.has_client_filename()
    assert not upload.has_client_media_type()


def test_an_upload_answers_with_its_stream() -> None:
    stream = make_stream("payload")

    assert UploadedFile(stream=stream).get_stream() is stream


def test_an_upload_opens_the_file_it_names(tmp_path: Path) -> None:
    path = tmp_path / "upload.txt"
    path.write_bytes(b"payload")

    assert UploadedFile(file=str(path)).get_stream().get_contents() == b"payload"


def test_an_upload_that_reports_a_failure_gives_no_stream() -> None:
    with pytest.raises(UploadedFileUploadErrorException, match="carried no file"):
        UploadedFile(upload_error=UploadError.NO_FILE).get_stream()


def test_the_upload_error_exception_names_the_error() -> None:
    exception = UploadedFileUploadErrorException(UploadError.INI_SIZE)

    assert exception.get_upload_error() is UploadError.INI_SIZE
    assert "larger than the size the server allows" in str(exception)


def test_an_upload_moves_to_a_path(tmp_path: Path) -> None:
    target = tmp_path / "moved.txt"
    upload = UploadedFile(stream=make_stream("payload"))

    upload.move_to(str(target))

    assert target.read_bytes() == b"payload"


def test_an_upload_moves_once(tmp_path: Path) -> None:
    upload = UploadedFile(stream=make_stream("payload"))
    upload.move_to(str(tmp_path / "first.txt"))

    with pytest.raises(UploadedFileAlreadyMovedException, match="already been moved"):
        upload.move_to(str(tmp_path / "second.txt"))


def test_an_upload_gives_no_stream_once_it_moved(tmp_path: Path) -> None:
    upload = UploadedFile(stream=make_stream("payload"))
    upload.move_to(str(tmp_path / "first.txt"))

    with pytest.raises(UploadedFileAlreadyMovedException, match="retrieve stream"):
        upload.get_stream()


def test_an_upload_refuses_a_directory_that_holds_nothing(tmp_path: Path) -> None:
    upload = UploadedFile(stream=make_stream("payload"))

    with pytest.raises(UploadedFileInvalidDirectoryException, match="does not exists or is not writable"):
        upload.move_to(str(tmp_path / "missing" / "moved.txt"))


def test_an_upload_that_reports_a_failure_moves_nowhere(tmp_path: Path) -> None:
    with pytest.raises(UploadedFileUploadErrorException):
        UploadedFile(upload_error=UploadError.CANT_WRITE).move_to(str(tmp_path / "moved.txt"))


def test_the_collection_holds_each_upload() -> None:
    upload = UploadedFile(stream=make_stream("a"))
    collection = UploadedFileCollection({"first": upload})

    assert collection.has("first")
    assert collection.get("first") is upload
    assert collection.get_all() == {"first": upload}


def test_the_collection_names_an_upload_it_does_not_hold() -> None:
    with pytest.raises(UploadedFileInvalidKeyException, match="does not exist"):
        UploadedFileCollection().get("first")


def test_the_collection_answers_with_copies() -> None:
    upload = UploadedFile(stream=make_stream("a"))
    collection = UploadedFileCollection()

    added = collection.with_file("first", upload)

    assert added.has("first")
    assert not collection.has("first")
    assert not added.without_file("first").has("first")


def test_a_server_request_carries_no_upload_by_default() -> None:
    assert ServerRequest().get_uploaded_files().get_all() == {}


def test_a_server_request_carries_the_uploads_it_is_given() -> None:
    upload = UploadedFile(stream=make_stream("a"))
    request = ServerRequest(uploaded_files=UploadedFileCollection({"first": upload}))

    assert request.get_uploaded_files().get("first") is upload


def test_with_uploaded_files_returns_a_copy() -> None:
    request = ServerRequest()
    files = UploadedFileCollection({"first": UploadedFile(stream=make_stream("a"))})

    changed = request.with_uploaded_files(files)

    assert changed.get_uploaded_files() is files
    assert request.get_uploaded_files() is not files


def make_json_headers() -> HeaderCollection:
    return HeaderCollection(Header(HeaderName.CONTENT_TYPE, ContentTypeValue.APPLICATION_JSON))


def test_a_json_request_reads_the_json_of_its_body() -> None:
    request = JsonServerRequest(body=make_stream('{"a":1}'), headers=make_json_headers())

    assert request.get_parsed_json().get("a") == 1


def test_a_json_request_reads_nothing_from_another_content_type() -> None:
    request = JsonServerRequest(body=make_stream('{"a":1}'))

    assert request.get_parsed_json().get_all() == {}


def test_a_json_request_reads_nothing_from_an_empty_body() -> None:
    request = JsonServerRequest(body=make_stream(""), headers=make_json_headers())

    assert request.get_parsed_json().get_all() == {}


def test_a_json_request_reports_a_body_that_holds_no_json() -> None:
    with pytest.raises(HttpRequestInvalidJsonException, match="holds no json"):
        JsonServerRequest(body=make_stream("not json"), headers=make_json_headers())


def test_a_json_request_reports_json_that_names_no_object() -> None:
    with pytest.raises(HttpRequestInvalidJsonException, match="names no object"):
        JsonServerRequest(body=make_stream("[1,2]"), headers=make_json_headers())


def test_a_json_request_takes_the_json_the_caller_gives() -> None:
    request = JsonServerRequest(parsed_json=ParsedJsonParamCollection({"a": 1}))

    assert request.get_parsed_json().get("a") == 1


def test_with_parsed_json_returns_a_copy() -> None:
    request = JsonServerRequest()
    params = ParsedJsonParamCollection({"a": 1})

    changed = request.with_parsed_json(params)

    assert changed.get_parsed_json() is params
    assert request.get_parsed_json() is not params


def test_a_copy_keeps_the_upload_error() -> None:
    exception = UploadedFileUploadErrorException(UploadError.PARTIAL)

    assert copy(exception).get_upload_error() is UploadError.PARTIAL
    assert str(loads(dumps(exception))) == str(exception)


def test_an_upload_that_names_neither_a_file_nor_a_stream_reports_so() -> None:
    # The constructor refuses this, so only a subclass that replaces it gets here.
    with pytest.raises(UploadedFileInvalidUploadedFileException, match="One of file or stream"):
        FilelessUploadFixture().get_stream()


def test_an_upload_reports_a_target_it_cannot_write(tmp_path: Path) -> None:
    upload = UploadedFile(stream=make_stream("payload"))

    # The target names a directory, so the open fails rather than the directory check.
    with pytest.raises(UploadedFileUnableToWriteFileException, match="Unable to write the upload"):
        upload.move_to(str(tmp_path))


def test_a_param_collection_refuses_a_param_it_cannot_carry() -> None:
    with pytest.raises(HttpParamInvalidParamException, match="scalar, None, or a collection"):
        QueryParamCollection({"a": ["not", "scalar"]})


def test_a_param_collection_takes_a_scalar_none_and_a_nested_collection() -> None:
    nested = QueryParamCollection({"b": "c"})
    collection = QueryParamCollection({"a": "value", "n": nested})

    assert collection.get("a") == "value"
    assert isinstance(collection.get("n"), QueryParamCollection)


def test_a_param_collection_answers_an_absent_key_with_its_default() -> None:
    assert QueryParamCollection().get("missing") == ""
    assert ParsedJsonParamCollection().get("missing") is None


def test_a_param_collection_gives_a_copy_of_a_nested_collection() -> None:
    nested = QueryParamCollection({"b": "c"})
    collection = QueryParamCollection({"n": nested})

    read = collection.get("n")

    assert read is not nested
    assert isinstance(read, QueryParamCollection)
    assert read.get("b") == "c"


def test_with_added_refuses_a_param_it_cannot_carry() -> None:
    with pytest.raises(HttpParamInvalidParamException):
        QueryParamCollection().with_added({"a": {"nested": "dict"}})


def test_with_refuses_a_param_it_cannot_carry() -> None:
    with pytest.raises(HttpParamInvalidParamException):
        QueryParamCollection().with_({"a": object()})
