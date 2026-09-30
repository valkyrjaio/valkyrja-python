# Container

## Introduction

The Container component holds the service container. The container binds a
service to an id, and it resolves that service when an application asks for the
id. A service provider gives a publisher for each service, and the container
calls that publisher once.

## Binding Keys Are Strings

Every id is a string constant, never a class object. A class object as a key
forces the module of that class to load, which defeats the reason the container
defers the load.

```python
# Wrong — the class object forces `user_repository` to import at binding time.
container.bind(UserRepository, lambda c, a: UserRepository())
```

```python
# Right — the string names the service, and no module loads.
container.bind(
    AppServiceId.USER_REPOSITORY,
    lambda c, a: UserRepository(c.get_singleton(AppServiceId.DATABASE)),
)
```

An application declares its own keys the same way. `AppServiceId` above is a
class that the application owns; the framework owns `ContainerServiceId`.

Read [`CONTAINER_BINDINGS.md`](https://github.com/valkyrjaio/architecture/blob/master/CONTAINER_BINDINGS.md)
for the full rule. Go and TypeScript use string keys for the same reason.

## Resolution Order

`get` looks for the service in one order:

1. A singleton instance that the container resolved already.
2. A service factory.
3. An alias, which points at another id.
4. The fallback.

Warning: the container tests each step for `None`, never for a false value. PHP
chains the steps with `??`, which tests for null alone. Python's `or` tests for a
false value, so a service that is an empty list would fall through to the next
step.

## The Fallback

Warning: the fallback always raises `ContainerInvalidReferenceException`. It
raises for `InvalidReferenceMode.NEW_INSTANCE_OR_THROW_EXCEPTION` too.

An id is a string constant such as `valkyrja.container.manager.ContainerContract`.
That string names no Python module, so the container cannot construct the class
that the id stands for. PHP constructs it, because a PHP id is a class name.
Java constructs it, because a Java id is a class object. TypeScript raises, for
the same reason as Python.

`InvalidReferenceMode` stays for parity with the other ports, and an entry that
resolves an id to a class can override `_get_fallback`.

## The Containers

| Class                  | Reads the parent through | Use                                          |
| ---------------------- | ------------------------ | -------------------------------------------- |
| `Container`            | —                        | the container of the application             |
| `ChildContainer`       | `ContainerContract`      | any parent, at the cost of a method call     |
| `NativeChildContainer` | the state of the parent  | a `Container` parent, at one dictionary read |

`ChildContainer` holds its own singleton bindings, so a service that the child
resolves stays apart from the parent. The child does reuse a singleton that the
parent resolved already, because a resolved instance is safe to share.

`ChildContainer` takes only the singletons and the callbacks of its
`ContainerData`. An alias or a service in that data would make the child resolve
what the parent owns, and the parent caches what it resolves, so the child would
write to the parent.

### The Child Never Writes To The Parent

A request-scoped child shares the parent between requests, so a write to the
parent outlives the request that made it. The child refuses a delegation that
would write:

- The parent holds a publish callback it has not run. The delegation would run
  that callback, and the parent would cache the result. The child answers from
  its own maps, and it raises
  `ContainerUnpublishedParentTargetException` when no map of its own answers.
- An alias of the parent reaches an id that the parent has not resolved. The
  child walks the alias chain first, and it raises
  `ContainerUnresolvedParentAliasException` when the walk reaches such an id.

Resolve or publish each such service before the request loop begins.

## Providers

A service provider gives one publisher for each service. The publisher is a
plain method reference, and the container calls it the first time an application
asks for the service:

```python
class AppServiceProvider(ServiceProviderContract):
    @override
    def publishers(self) -> dict[str, PublishCallback]:
        return {AppServiceId.USER_REPOSITORY: AppServiceProvider.publish_user_repository}

    @staticmethod
    def publish_user_repository(container: ContainerContract) -> None:
        container.set_singleton(AppServiceId.USER_REPOSITORY, UserRepository())
```

Warning: `register` raises `ContainerInvalidPublishCallbackException` when a
publisher is not callable.

## Cache

`ContainerData` holds the state of a container. `get_data` returns the state,
and `set_from_data` adds a state to the container. `sindri` writes this same
shape into the generated cache, so the container loads a cache the way it loads
its own state.

## Exceptions

- `ContainerRuntimeException` — the base runtime exception, abstract
- `ContainerInvalidArgumentException` — the base invalid argument exception, abstract
- `ContainerInvalidReferenceException` — the container has no service for the id
- `ContainerInvalidPublishCallbackException` — a provider gives a publisher that
  the container cannot call
- `ContainerUnpublishedParentTargetException` — a child would run a publish
  callback of the parent
- `ContainerUnresolvedParentAliasException` — an alias of the parent reaches an
  id that the parent has not resolved
