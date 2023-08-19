#!/usr/bin/env python3

# *- IMPORTS -* #

# for `QodexNamespace` abstract methods
import abc

# for `parse_args()`
import argparse

# exit codes like `EX_OK`
import os

# `Any`, `cast`, `TextIO`
import typing

# *- ======= -* #

# *- CONSTANTS -* #

# No constants yet.

# *- ========= -* #

# *- TYPES -* #


class QodexNamespace(typing.Protocol):
    """
    Used like `argparse.Namespace`, but our arguments are typed.

    ## Why it is nice

    This allows us to have typed command line arguments when we
    pass them to the rest of the program.

    ## Why it can be a burden

    One downside is that it duplicates maintenance because
    every time an argument is added in `parse_args()`, it must be
    added here as well and with the correct type hinting. And the
    latter isn't always obvious because of some mechanics like
    `nargs`.
    """

    files: list[typing.TextIO]

    # *- `argparse.Namespace` stuff -* #

    @abc.abstractmethod
    def _get_args(self) -> list[typing.Any]:
        """
        Private method to get a list of the positional arguments.

        Implemented by `argparse.Namespace`.
        """

    @abc.abstractmethod
    def _get_kwargs(self) -> list[tuple[str, typing.Any]]:
        """
        Private method to get a list of a key/value pair of the named
        arguments.

        Implemented by `argparse.Namespace`.
        """


# *- ===== -* #

# *- FUNCTIONS -* #


def parse_args() -> QodexNamespace:
    """
    Parses command line arguments using the standard library `argparse`.

    At runtime, it returns an `argparse.Namespace` object, but for
    type-checking purposes, we virtually cast it to a custom protocol.

    In other words, we make type-checkers believe it returns a
    `QodexNamespace` object so e.g. `args.files` isn't a plain
    `typing.Any` but really `list[typing.TextIO]`.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(  # pyright: ignore[reportUnusedCallResult]
        "files",
        nargs="*",
        type=argparse.FileType("r+"),
    )

    # The cast is necessary here, because `argparse.Namespace` is not
    # considered to have e.g. a `files` attribute despite having it at
    # runtime, hence we have to convince type-checkers that it is a
    # `QodexNamespace`. A `type: ignore` comment could be used as well
    # but I don't think it makes sense here because it's not a
    # "ignore this type incompatibility" but rather "it actually fulfills
    # `QodexNamespace` requirements but you cannot be aware of that"
    return typing.cast(QodexNamespace, parser.parse_args())


def main() -> int:
    """
    Entry point of the Qodex program.

    This is the function that gets called when running `qodex` in the
    shell.
    """

    args = parse_args()

    print("Hello Qodex!")

    return os.EX_OK


# *- ========= -* #
