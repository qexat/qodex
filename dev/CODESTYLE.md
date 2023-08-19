# Code style guidelines

In this project, we use [tools](#tools) that already provide sets of style
rules, but there are additional details that are not covered by them that we
will try to address in this document:

- [File structure](#file-structure)
  - [Add structure commentary](#add-structure-commentary)
- [Comments](#comments)
  - [Explain your intents](#explain-your-intents)
- [Imports](#imports)
  - [Avoid `from ... import` import kind when unnecessary](#avoid-from--import-import-kind-when-unnecessary)
  - [Split imported symbols to different lines](#split-imported-symbols-to-different-lines)

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
