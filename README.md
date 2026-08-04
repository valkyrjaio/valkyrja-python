<p align="center"><a href="https://valkyrja.io" target="_blank">
    <img src="https://raw.githubusercontent.com/valkyrjaio/art/refs/heads/master/long-banner/orange/python.png" width="100%">
</a></p>

# Valkyrja

[Valkyrja][Valkyrja url] is a Python framework for web and console applications.

Valkyrja (pronounced "Valk-ear-ya") is the Old Norse spelling for Valkyrie, a
mythical creature that would guide warriors to Valhalla (the afterlife and a
better place) after death. In a similar sense, the Valkyrja framework guides
your application to be in a better state. Fast, light, and robust, Valkyrja
does the heavy lifting so you can focus on your application.

<p>
    <a href="https://pypi.org/project/valkyrja/"><img src="https://img.shields.io/pypi/v/valkyrja.svg" alt="Latest Version on PyPI"></a>
    <a href="https://pypi.org/project/valkyrja/"><img src="https://img.shields.io/pypi/pyversions/valkyrja.svg" alt="Supported Python Version"></a>
    <a href="https://github.com/valkyrjaio/valkyrja-python/blob/26.x/LICENSE.md"><img src="https://img.shields.io/github/license/valkyrjaio/valkyrja-python.svg" alt="License"></a>
    <a href="https://github.com/valkyrjaio/valkyrja-python/actions/workflows/ci.yml?query=branch%3A26.x"><img src="https://github.com/valkyrjaio/valkyrja-python/actions/workflows/ci.yml/badge.svg?branch=26.x" alt="CI Status"></a>
</p>

Status
------

Warning: the Python port is in progress. This repository holds the package, the
CI pipeline, and the release process. It does not hold the framework yet. Install
the package to reserve the dependency, and do not build an application on it yet.

PHP is the reference implementation, and every other port mirrors its structure,
its naming, and its tests. Read [`PORTS.md`][ports url] for the state of each
language.

What Valkyrja Includes
----------------------

The list below is what the port delivers. Each item exists in the PHP reference
implementation today.

- **HTTP and CLI entry points** — one application architecture serves a web
  request and a command-line invocation
- **Dependency injection container** — deferred bindings, contextual resolution,
  and a generated cache that the framework loads at boot
- **Routing** — route definitions with middleware, constraints, and reverse
  resolution
- **Event dispatcher** — decoupled event handling with typed listeners
- **ASGI worker support** — Uvicorn, Hypercorn, and Granian entry points, and a
  CGI and Lambda mode

The framework works without a cache. A provider exposes its class references, so
the framework walks the provider tree and registers everything at runtime. The
cache is a cold-start optimization, and it is not a correctness requirement.

Installation
------------

```bash
uv add valkyrja
```

```bash
pip install valkyrja
```

**Python 3.14 or later is required.**

Ecosystem
---------

Valkyrja is the core framework. A set of related projects sits around it in the
Valkyrjaio organization:

- [**Sindri**][sindri url] — the build tool that generates the cache. It is a
  development dependency, and it never ships to production.
- [**Valkyrja Ruff**][ci ruff url] — the shared Ruff configuration, and the
  copyright header command that every Valkyrja Python repository consumes
- [**Project Template**][template url] — the scaffold that a new Valkyrja Python
  repository starts from

See the [Valkyrjaio organization page][org url] for the complete listing.

Versioning and Release Process
------------------------------

Valkyrja follows [semantic versioning][semantic versioning url] with a major
release every year, and support for each major version for 2 years from the date
of release.

For more information see the
[Versioning and Release Process documentation][versioning url].

Contributing
------------

Valkyrja is an open-source, community-driven project. Thank you for your interest
in helping develop, maintain, and release it.

See [`CONTRIBUTING.md`][contributing url] for the submission process and
[`VOCABULARY.md`][vocabulary url] for the terminology that Valkyrja uses.

Security Issues
---------------

If you discover a security vulnerability within Valkyrja, please follow the
[disclosure procedure][security vulnerabilities url].

License
-------

Valkyrja is open-source software licensed under the
[MIT license][MIT license url]. See [`LICENSE.md`](./LICENSE.md).

[Valkyrja url]: https://valkyrja.io
[org url]: https://github.com/valkyrjaio
[sindri url]: https://github.com/valkyrjaio/sindri-php
[ci ruff url]: https://github.com/valkyrjaio/ci-ruff-python
[template url]: https://github.com/valkyrjaio/project-template-python
[ports url]: https://github.com/valkyrjaio/architecture/blob/26.x/PORTS.md
[versioning url]: https://github.com/valkyrjaio/architecture/blob/26.x/VERSIONING.md
[contributing url]: https://github.com/valkyrjaio/.github/blob/26.x/CONTRIBUTING.md
[vocabulary url]: https://github.com/valkyrjaio/.github/blob/26.x/VOCABULARY.md
[security vulnerabilities url]: https://github.com/valkyrjaio/.github/blob/26.x/SECURITY.md
[semantic versioning url]: https://semver.org/
[MIT license url]: https://opensource.org/licenses/MIT
