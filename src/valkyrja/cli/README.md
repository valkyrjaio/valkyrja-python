# Cli

## Introduction

The Cli component runs a command from the command line. It holds one
sub-component for each part of that work, and each sub-component keeps its own
contracts, binding keys, and throwables.

| Sub-component | Holds                                                     |
| ------------- | --------------------------------------------------------- |
| `interaction` | the input, the output, a message, and a question          |
| `middleware`  | a handler for each stage that a command passes            |
| `routing`     | a command, its parameters, and the router that matches it |
| `server`      | the input handler that runs a command, and the exiter     |

## Interaction

### Input And Output

An input reads the arguments and the options that the command line gave. An
output holds the messages that a command writes, and it writes each one when the
command asks:

```python
output = output_factory.create_output().with_added_message(Message("Done"))
output = output.write_messages()
```

An output is immutable. Every `with_` method answers with a copy, so a command
that writes passes the new output on.

### The Kinds Of Output

| Contract               | Writes                                   |
| ---------------------- | ---------------------------------------- |
| `OutputContract`       | the standard output                      |
| `PlainOutputContract`  | the standard output, with no ANSI format |
| `EmptyOutputContract`  | nothing                                  |
| `FileOutputContract`   | a file                                   |
| `StreamOutputContract` | a stream that the caller gives           |

`OutputFactoryContract` builds each one, and it reads
`CliInteractionConfigContract` for the three flags that every output carries:
`is_interactive`, `is_quiet`, and `is_silent`.

### Quiet, Silent, And Interactive

- `is_silent` writes no message at all.
- `is_quiet` writes no message while the exit code is `ExitCode.SUCCESS`, so a
  failure still reports.
- `is_interactive` asks a question of the user. A non-interactive output takes
  the answer that the question already holds.

### Messages And Questions

A message carries text and a formatter. A question carries the text, the answer
it expects, and the handler that runs once the user answers. `QuestionWriter`
writes a question, reads the answer, and asks again while the answer is not one
the question allows.

### Binding Keys

| Constant                                          | Binds                          |
| ------------------------------------------------- | ------------------------------ |
| `CliInteractionServiceId.INPUT_CONTRACT`          | `InputContract`                |
| `CliInteractionServiceId.OUTPUT_CONTRACT`         | `OutputContract`               |
| `CliInteractionServiceId.OUTPUT_FACTORY_CONTRACT` | `OutputFactoryContract`        |
| `CliInteractionServiceId.CONFIG_CONTRACT`         | `CliInteractionConfigContract` |

## Middleware

A command passes several stages, and each stage has a handler. A middleware is
bound in the container by its own key, and a handler resolves it by that key:

| Stage               | Runs when                           |
| ------------------- | ----------------------------------- |
| `input_received`    | the input arrives, before any match |
| `route_matched`     | a command matches the input         |
| `route_not_matched` | no command matches the input        |
| `route_dispatched`  | the command answered with an output |
| `throwable_caught`  | a stage raised                      |
| `process_exiting`   | the run ends                        |

A handler appends each middleware, and it never removes a duplicate. A middleware
that a caller adds twice runs twice, which is the caller's own doing.

## Routing

A command is a route. It carries a name, a description, a handler, and the
parameters it takes:

```python
class Controller:
    @staticmethod
    @route(name="greet", description="Greet one person")
    def greet(container: ContainerContract, route: RouteContract) -> OutputContract: ...
```

A handler takes the container and the route. The route carries every parameter the
command took, so the handler reads a value from it:

```python
name = route.get_argument_value("name")
```

`AttributeRouteCollector.get_routes` reads each marked function of each class it is
given, and a command that a base class declares is read as well.

Warning: a marked member is a static method. A handler takes the container and the
arguments alone, so a member that also takes an instance cannot answer a command.

### Parameters

An argument takes its value from the position it sits in, and an option takes its
value from the name the command line gives:

| Parameter           | Reads                                       |
| ------------------- | ------------------------------------------- |
| `ArgumentParameter` | one value, or every remaining value         |
| `OptionParameter`   | a value that a name or a short name carries |

A parameter holds its raw values, and it applies no cast of its own. `CasterContract`
takes a parameter and answers with its values, with the cast applied:

```python
caster = container.get(CliRoutingServiceId.CASTER_CONTRACT)
values = caster.get_cast_values(parameter)
```

A parameter is a data object, so it holds no container. The thing that asks for a
cast value does the casting.

Warning: the caster asks the container for a service, never for a singleton. A
singleton would build one type from the first value and hand it back for every
later value.

## Server

`InputHandler` runs one command. It gives the input to the input received stage,
then to the router, then it writes the output and ends the process:

```python
InputHandler(...).run(InputFactory.from_globals(sys.argv))
```

Each stage of the run sits under a guard, and a stage that raises takes a report
rather than the process. A report that fails itself takes a second report, which
the handler builds without the output factory, so no configured factory redirects
it and no flag suppresses it.

### The Commands It Ships

| Command     | Does                                          |
| ----------- | --------------------------------------------- |
| `list:bash` | writes each command name, for bash completion |

`CheckForHelpOptionsMiddleware` sends an input that carries `--help` to the help
command, and it carries the original command name as a `command` option.
`CheckCommandForTypoMiddleware` offers a command whose name is close to the one
the input names.

## Exit Codes

`ExitCode` holds the conventional codes that a command returns. `SUCCESS` is `0`,
`ERROR` is `1`, and the codes from `64` upward follow the `sysexits` convention.
`AUTO_EXIT` is `255`.

## Throwables

Each sub-component keeps its own base pair, and each pair chains through the
base pair of the component:

```
ValkyrjaRuntimeException
└── CliRuntimeException
    └── CliInteractionRuntimeException
```

A caller that catches `CliRuntimeException` therefore catches a failure of any
sub-component. `CliThrowable` marks every throwable of the component, and each
sub-component narrows it with a contract of its own.

Read [`THROWABLES.md`](https://github.com/valkyrjaio/architecture/blob/master/THROWABLES.md)
for the naming rule.
