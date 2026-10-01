# Http

## Introduction

The Http component holds the message types that a server reads and writes. It
holds one sub-component for each part of that work, and each sub-component keeps
its own contracts and throwables.

| Sub-component | Holds                                                       |
| ------------- | ----------------------------------------------------------- |
| `message`     | the request, the response, the headers, the uri, the stream |

## A Body Is Bytes

Every body is a stream of bytes, never text. `write` takes bytes, and it takes a
string that it encodes as UTF-8. `read` and `get_contents` answer with bytes:

```python
body = Stream()
body.write("a string")
body.rewind()

assert body.get_contents() == b"a string"
assert str(body) == "a string"
```

`str()` decodes the whole stream from the start, so a reader that wants text asks
for it once.

Warning: `close` leaves a stream of the process open. The process owns `stdin`,
`stdout`, and `stderr`, so closing one of them takes it from every other reader.

## A Header Takes Only What RFC 7230 Allows

Every header name and every header value passes a check, and a value that would
split the response is refused:

```python
# Raises `HttpHeaderInvalidValueException`, because the fold opens a second header.
Header("Content-Type", "text/html\r\nX-Injected: yes")
```

`HeaderFactory` holds the check, and `get_filtered_value` answers with the value
that holds only the characters a header can carry.

A header is immutable. It answers array access and iteration, and it refuses a
write to one position:

```python
header = Header("Accept", "text/html", "application/json")

assert str(header[0]) == "text/html"
assert len(header) == 2
```

## A Uri Encodes Each Component

The constructor and every `with_` method filter what they take. Each component
allows the characters that RFC 3986 names for it, and the uri encodes the rest:

```python
assert Uri(path="/a b").get_path() == "/a%20b"
assert Uri(host="VALKYRJA.IO").get_host() == "valkyrja.io"
```

`Char` names the characters that each component allows. `UriFactory.from_string`
reads a uri from one string.

Warning: `get_port` answers zero for the port that the scheme implies, and for a
uri that names no host. A uri that writes itself therefore leaves the port out.

## A Response

| Class              | Carries                      |
| ------------------ | ---------------------------- |
| `Response`         | a body that a caller builds  |
| `TextResponse`     | plain text                   |
| `HtmlResponse`     | html                         |
| `XmlResponse`      | xml                          |
| `JsonResponse`     | json, and json in a callback |
| `EmptyResponse`    | no body                      |
| `RedirectResponse` | a `Location` header alone    |

`ResponseFactory` builds each one.

### Json

A json body escapes each character that a page reads as markup, so a page embeds
the body without closing a tag or an attribute. A forward slash stays as it is.
PHP writes the same json with the flags that add up to 79.

```python
assert str(JsonResponse({"a": "<b>"}).get_body()) == '{"a":"\\u003Cb\\u003E"}'
```

`with_callback` wraps the json for a caller that reads it as javascript, and the
content type becomes `text/javascript`, which an older browser also reads.

Warning: a number that json cannot hold reports a failure. A body that carried
the word for it would reach a reader that parses no such word.

## Throwables

Each sub-component keeps its own base pair, and each pair chains through the base
pair of the component:

```
ValkyrjaRuntimeException
└── HttpRuntimeException
    └── HttpMessageRuntimeException
        └── HttpStreamRuntimeException
```

A caller that catches `HttpRuntimeException` therefore catches a failure of any
sub-component.

Read [`HTTP_MESSAGE.md`](https://github.com/valkyrjaio/architecture/blob/master/HTTP_MESSAGE.md)
for the cross-language map of the message types.
