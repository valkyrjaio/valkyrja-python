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
