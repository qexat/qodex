# Code style guidelines

In this project, we use [tools](#tools) that already provide sets of style
rules, but there are additional details that are not covered by them that we
will try to address in this document:

- [File structure](#file-structure)
  - [Add structure commentary](#add-structure-commentary)
- [Comments](#comments)
  - [Explain your intents](#explain-your-intents)
  - [Do not over-comment](#do-not-over-comment)
- [Imports](#imports)
  - [Avoid `from ... import` import kind when unnecessary](#avoid-from--import-import-kind-when-unnecessary)
  - [Split imported symbols to different lines](#split-imported-symbols-to-different-lines)
  - [Do not use aliases](#do-not-use-aliases)
- [Code logic](#code-logic)
  - [Avoid reinventing the wheel](#avoid-reinventing-the-wheel)

## Tools

- Code formatter: [Black](https://github.com/psf/black/)
- Linter: [Ruff](https://github.com/astral-sh/ruff/)

Both have their respective Visual Studio Code extensions if you happen to use
this editor.

## Additional guidelines

### File structure

It is very likely that files will have the following scheme:

- Imports
- Constants
- Types (classes, type variables...)
- Functions

#### Add structure commentary

Make clear where each section starts and ends. I personally use the VS Code
extension called [Better Comments](https://github.com/aaron-bond/better-comments), which makes comments green if they start with a `*`.

For this reason, my section comment usually follows this pattern:

```py
# *- SECTION_NAME -* #

...

# *- ============ -* #
```

I do not specifically enforce the asterisks, but it would be _slightly_
annoying if everyone starts [creating their own](https://xkcd.com/927/) way
to split sections.

---

### Comments

#### Explain your intents

Casting a returned value to a type for better type-checking? **Explain why you
do so!** It is also worth writing a long comment if **there are other
alternatives** to do the same thing that have been considered but not chosen.

```py
  ...
  93  │     # The cast is necessary here, because `argparse.Namespace` is not
  94  │     # considered to have e.g. a `files` attribute despite having it at
  95  │     # runtime, hence we have to convince type-checkers that it is a
  96  │     # `QodexNamespace`. A `type: ignore` comment could be used as well
  97  │     # but I don't think it makes sense here because it's not a
  98  │     # "ignore this type incompatibility" but rather "it actually fulfills
  99  │     # `QodexNamespace` requirements but you cannot be aware of that"
 100  │     return typing.cast(QodexNamespace, parser.parse_args())
  ...
```

People may read (and write) code in a decade, and they have to be **aware of
the choices made** and the reason behind: otherwise, they might change or
remove something that might cause a subtle and quiet issue (this includes
third-party tools such as type-checkers, by the way).

#### Do not over-comment

Commenting is good, but like most things, overdoing it can reverse the positive
effects, especially when you are describing _what_ you do rather than
[_why_](#explain-your-intents).

A terrible example of that:

```py
  ...
 31   │ num_sum = 0
 32   │ # We iterate over the numbers
 33   │ for num in nums:
 34   │     # we add the current number to the sum
 35   │     num_sum += num
  ...
```

Sorry for the harsh truth, but these two comments are absolutely unnecessary.
They transcribe something that we can already see by reading the code itself,
which is so simple that even people who are not familiar with Python would
very likely understand.

See also: [Avoid reinventing the wheel](#avoid-reinventing-the-wheel)

---

### Imports

#### Avoid `from ... import` import kind when unnecessary

A large amount of symbols from modules do not carry their origin by their sole
name. It also allows to visually distinguish a symbol in the current module
from an imported one.

Example:

```py
  ...
 4    │ from argparse import ArgumentParser, FileType, Namespace
  ...
 18   │ def parse_args() -> Namespace:
 19   │     parser = ArgumentParser()
 20   │     parser.add_argument("file", type=FileType("r"))
 21   │
 22   │     return parser.parse_args()
  ...
```

Maybe it is obvious to you that `ArgumentParser`, `FileType` and `Namespace`
are coming from the `argparse` module, but this might not be the case for other
developers. It is not necessarily bad nor always avoidable, but I tend to
prefer avoiding context-sensitive names. Even though it often makes shorter
lines of code, I think that it decreases readability more often than the
opposite.

Here is the same example with guidelines applied:

```py
  ...
 4    │ # even better: comment why/what you are using the module!
 5    │ import argparse
  ...
 19   │ def parse_args() -> argparse.Namespace:
 20   │     parser = argparse.ArgumentParser()
 21   │     parser.add_argument("file", type=argparse.FileType("r"))
 22   │
 23   │     return parser.parse_args()
  ...
```

Note: this guideline does NOT apply to `__future__` imports.

#### Split imported symbols to different lines

In few rare cases, it may be impossible to use a plain `import`. If that
happens, separate the symbols in different lines, even if they come from
the same module. Although this has the downside of repeating code, you will
also never be mad again at git for a merge conflict because someone changed
an import in the same file you were working on.

Here is what I mean:

```py
  ...
 4    │ from argparse import ArgumentParser
 5    │ from argparse import FileType
 6    │ from argparse import Namespace
  ...
 20   │ def parse_args() -> Namespace:
 21   │     parser = ArgumentParser()
 22   │     parser.add_argument("file", type=FileType("r"))
 23   │
 24   │     return parser.parse_args()
  ...
```

#### Do not use aliases

Naming stuff is already one of the hardest things in programming. It is also
highly subjective ; for you, `t` might stands for `typing`, but someone might
associate the letter with another module. It is okay to split a line into
several ones, it does not necessarily make it less readable.

An example of what to avoid:

```py
 1    │ import typing as t
 2    │
 3    │ T = t.TypeVar("T")
  ...
 6    │ def my_function(data: list[T], index: int) -> t.Optional[T]:
                 # on a side note, use T | None instead ^^^^^^^^
  ...
```

As for `from ... import` imports, it obscures the origin of the symbols.
It is even worse in my opinion ; I'd rather use `from typing import ...` than
`import typing as t` 💀.

There is one exception for this rule, though. It is okay to use an alias if
you are importing a module that is a drop-in replacement of a standard library.

See also: [Avoid reinventing the wheel](#avoid-reinventing-the-wheel)

### Code logic

#### Avoid reinventing the wheel

CPython is the standard implementation of Python and it comes with "batteries
included". This means that you can find a lot of common programming patterns
already coded in the standard library. Use them as much as possible,
especially if they are written in C (it is faster 🚀).

```py
  ...
 31   │ num_sum = 0
 32   │ for num in nums:
 33   │     num_sum += num
  ...
```

Here, you can use the built-in `sum` on `nums` instead.

Okay, it is quite a silly example as it is very likely that you are aware of
the existence of such function, but the idea remains the same for modules that
you have to import.

```py
  ...
 31   │ num_sum = sum(nums)
      # ^^^^^^^ now I wonder why you need a variable for that
  ...
```

In extension to this guideline, you can also use third-packages as drop-in
replacements of built-in modules if they have specific features that you need.

For example, I often use [`regex`](https://github.com/mrabarnett/mrab-regex)
instead of the built-in module `re`. It is literally designed as an extension
of the latter, and has way better features (in my opinion) while supporting
backward compatibility.
