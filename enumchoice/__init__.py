"""Enum Choice for Click."""

__author__ = """Maxim Zaslavsky"""
__email__ = "maxim@maximz.com"
__version__ = "0.0.1"

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())

from enum import Enum

import click


class EnumChoice(click.Choice):
    """
    Expose Enum options within a click Choice option, using the names of the enum options.

    based on https://github.com/pallets/click/issues/605#issuecomment-917022108 - but lookup by name instead of by value

    Suppose you have an enum called ColorEnum.

    WITHOUT THIS, you would do something like this to expose ColorEnum choices in a Click CLI:
        @click.option(
            "--color",
            multiple=True,
            default=list(ColorEnum),
            show_default=True,
            type=click.Choice([c.name for c in ColorEnum], case_sensitive=False)
        )
        def func(color):
            ...
            color = [ColorEnum[c] if isinstance(c, str) else c for c in color]

    Instead, simply use this (after `from enumchoice import EnumChoice`):
        @click.option(
            "--color",
            multiple=True,
            default=list(ColorEnum),
            show_default=True,
            type=EnumChoice(ColorEnum, case_sensitive=False),
        )  # if multiple isn't True, default could be 'red' or ColorEnum.red
    """

    def __init__(self, enum: Enum, case_sensitive=False):
        self.__enum = enum
        super().__init__(
            choices=[item.name for item in enum], case_sensitive=case_sensitive
        )

    def convert(self, value, param, ctx):
        if value is None or isinstance(value, Enum):
            return value

        converted_str = super().convert(value, param, ctx)
        return self.__enum[converted_str]
