# Event

## Introduction

The Event component dispatches an event to each listener that waits for it. A
listener names the event it waits for, it carries a unique name, and it carries
a handler that the dispatcher calls.

## An Event Answers Its Own Id

Every event carries its own id, and `get_event_id` returns it. The id is the
same string constant that the container binds.

```python
class OrderPlaced(EventContract):
    @override
    def get_event_id(self) -> str:
        return AppEventId.ORDER_PLACED
```

PHP and Java identify an event by its class, because a PHP id is a class name
and a Java id is a class object. A Python id is a string, and that string names
no class, so the event answers for itself. Go identifies an event the same way.

Warning: the id of the event must equal the key that the container binds. The
dispatcher raises `EventInvalidEventException` when a key resolves to an event
that names a different id, because the listeners of the key would never run.

## Binding Keys

| Constant                             | Binds                        |
| ------------------------------------ | ---------------------------- |
| `EventServiceId.EVENT_DATA`          | `EventData`                  |
| `EventServiceId.COLLECTION_CONTRACT` | `ListenerCollectionContract` |
| `EventServiceId.COLLECTOR_CONTRACT`  | `ListenerCollectorContract`  |
| `EventServiceId.DISPATCHER_CONTRACT` | `EventDispatcherContract`    |

Read [`CONTAINER_BINDINGS.md`](https://github.com/valkyrjaio/architecture/blob/master/CONTAINER_BINDINGS.md)
for the rule that shapes each key.

## The Event Contracts

An event implements `EventContract`, and it adds a contract for each capability
it needs:

| Contract                           | Adds                                              |
| ---------------------------------- | ------------------------------------------------- |
| `EventContract`                    | the id of the event                               |
| `ArgumentsCapableEventContract`    | the dispatcher sets the arguments on the event    |
| `DispatchCollectableEventContract` | the event keeps what each listener returned       |
| `StoppableEventContract`           | the event stops the listeners after it, as PSR-14 |

## Listeners

A listener is a data object. It names an event, it carries a unique name, and it
carries a handler:

```python
listener = Listener(AppEventId.ORDER_PLACED, "mail.order_placed", send_mail)
```

The name is unique across the collection, so a second listener that carries a
name replaces the first.

A handler takes the container and a map of arguments, and the dispatcher puts the
event in that map under `EventArgument.EVENT`:

```python
def send_mail(container: ContainerContract, arguments: dict[str, Any]) -> None:
    event = arguments[EventArgument.EVENT]
```

## Cache

`EventData` holds the state of a collection. `events` maps an event id to the
names of its listeners, and `listeners` maps a name to a factory that builds the
listener. `sindri` writes this same shape into the generated cache.

## Exceptions

- `EventRuntimeException` — the base runtime exception, abstract
- `EventInvalidArgumentException` — the base invalid argument exception, abstract
- `EventInvalidEventException` — a binding key resolves to a thing that is not
  the event the key names
