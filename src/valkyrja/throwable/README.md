# Throwable

## Introduction

The Throwable component holds the exception hierarchy of the framework. It
defines a contract that adds a trace code to Python's `BaseException`, the two
abstract base exceptions that every component extends, and the contract for the
handler that catches an unhandled throwable.

## The Throwable Contract

`valkyrja.throwable.contract.valkyrja_throwable.ValkyrjaThrowable` extends
`BaseException` and adds one method:

```python
def get_trace_code(self) -> str: ...
```

A trace code identifies a failure point. A log entry carries the trace code, and
the application does not have to show the stack trace to a user.
`ThrowableFactory` computes the code from the class name and the stack trace:

```python
from valkyrja.throwable.factory.throwable_factory import ThrowableFactory

trace_code = ThrowableFactory.get_trace_code(exception)
```

An unraised throwable carries no traceback, so two unraised instances of one
class get the same code.

## Exception Classes

Two abstract base exceptions live under
`valkyrja.throwable.exception.abstract`:

- `ValkyrjaRuntimeException` — extends `RuntimeError`
- `ValkyrjaInvalidArgumentException` — extends `ValueError`

The name of each one keeps parity with the other ports, and the base keeps the
exception catchable the way the language catches it. Every component extends
these to get a `ComponentRuntimeException` and a
`ComponentInvalidArgumentException`. A concrete exception extends the component
class. Read [`THROWABLES.md`](https://github.com/valkyrjaio/architecture/blob/master/THROWABLES.md)
for the full hierarchy and the naming rule.

## Abstract Enforcement

Warning: `ABC` alone does not stop the instantiation of an exception class. Only
`object.__new__` reads `__abstractmethods__`, and `BaseException.__new__`
replaces it. An abstract exception with an unimplemented abstract method still
constructs.

`ValkyrjaThrowable` closes this. Each abstract class sets the
`_valkyrja_abstract` flag, and `__new__` reads the flag from the class itself,
never from a parent:

```python
# Wrong — the base class is abstract, so this raises TypeError.
raise ValkyrjaRuntimeException("The cache directory is not writable")
```

```python
# Right — a concrete exception names the problem.
raise ContainerNotFoundException("The container has no binding for the router")
```

Two rules follow for a subclass:

1. **An abstract subclass sets `_valkyrja_abstract = True`.** The flag does not
   inherit, so a class that omits it is concrete.
2. **`ValkyrjaThrowable` comes first in the base list.** The method resolution
   order decides which `__new__` runs. `RuntimeError` and `ValueError` inherit a
   `__new__` that constructs any class, so a base list that puts one of them
   first defeats the guard.

```python
# Wrong — `RuntimeError.__new__` wins, and the abstract class constructs.
class CacheRuntimeException(RuntimeError, ValkyrjaThrowable):
    _valkyrja_abstract = True
```

```python
# Right — `ValkyrjaRuntimeException` already orders the bases correctly.
class CacheRuntimeException(ValkyrjaRuntimeException):
    _valkyrja_abstract = True
```

## Catch Boundaries

The hierarchy gives a catch boundary at each level:

```python
# framework-wide — catch anything that Valkyrja raises
except ValkyrjaThrowable: ...

# framework category-wide — catch every runtime exception that Valkyrja raises
except ValkyrjaRuntimeException: ...

# language-wide — the language root still catches the exception
except ValueError: ...
```

## The Throwable Handler

`valkyrja.throwable.handler.contract.throwable_handler_contract.ThrowableHandlerContract`
defines the handler that catches an unhandled throwable:

```python
def enable(self, display_errors: bool = False) -> None: ...
```

`enable` registers the handler. Warning: a handler that displays an error shows
the internals of the application. Set `display_errors` in development only.

## Container Bindings

The component binds one service. `ThrowableServiceId` holds the key:

| Key | Value | Binds |
| --- | --- | --- |
| `ThrowableServiceId.HANDLER_CONTRACT` | `Valkyrja.Throwable.Handler.ThrowableHandlerContract` | the handler that catches an unhandled throwable |

A binding key is a string constant, never a class object. A class object as a
key forces the module of that class to load, and the container exists to defer
that load. The TypeScript port holds the same key, because both ports resolve a
service by string.
