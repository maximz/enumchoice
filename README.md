# enumchoice

`enumchoice` is a small helper for Click CLIs that lets a Python `Enum` be used
directly as an option type. It exposes enum member names as the accepted
command-line choices and returns the matching enum member to the Click command.

## Why it exists

Click's built-in `click.Choice` validates strings. If an option represents an
`Enum`, a command normally has to build a list of enum names for Click and then
convert the selected strings back to enum members. `EnumChoice` keeps those two
steps in one Click parameter type.

## Installation

```bash
pip install enumchoice
```

The package requires Python 3.8 or newer and Click 7.0 or newer.

## Usage

```python
from enum import Enum

import click
from enumchoice import EnumChoice


class Color(Enum):
    red = "r"
    blue = "b"
    green = "g"


@click.command()
@click.option("--color", type=EnumChoice(Color), default=Color.red, show_default=True)
def cli(color):
    assert isinstance(color, Color)
    click.echo(color.name)
```

Matching is case-insensitive by default, so `--color RED`, `--color red`, and
`--color ReD` all resolve to `Color.red`. Pass `case_sensitive=True` to require
exact enum member names.

`EnumChoice` also works with Click's `multiple=True` options:

```python
@click.option(
    "--color",
    multiple=True,
    default=list(Color),
    type=EnumChoice(Color),
)
def cli(color):
    # color is a tuple of Color members.
    ...
```

## How it works

`EnumChoice` subclasses `click.Choice`. Its constructor builds the choice list
from each enum member's `name`. During conversion it lets Click perform normal
choice validation and case normalization, then looks up the normalized name in
the enum class and returns that member.

`None` and already-converted `Enum` instances pass through unchanged, which
allows enum-valued defaults such as `default=Color.red` or `default=list(Color)`.

## Behavior and limitations

- Choices are enum member names, not enum values.
- Click callbacks receive enum members, not strings.
- No aliases are added beyond the enum's declared member names.
- The package metadata currently marks the project as pre-alpha, version
  `0.0.1`.

## Development

```bash
pip install -r requirements_dev.txt
pip install -e .
make test
make lint
make docs
```

The repository includes pytest, pre-commit, coverage, Sphinx documentation, and
release packaging configuration. The project is distributed under the MIT
license.
