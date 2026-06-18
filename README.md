# todo-comment-parser

Walk a directory tree and print every TODO-style comment block from every text file it finds.

A "TODO block" is the TODO line plus any immediately-following lines that share the same comment prefix. Files that mix more than one comment style (e.g. `# ` and `// ` TODOs in the same file) are rejected.

## Install

```bash
pip install .
```

This installs a `parsetodo` console script.

## Usage

```bash
parsetodo [--tag TAG] [--depth N] [--include PATTERN] DIRECTORY
```

| Flag | Default | Description |
| --- | --- | --- |
| `DIRECTORY` | *(required)* | Root directory to walk. |
| `--tag` | `TODO` | Token that marks a comment block. Use `FIXME`, `XXX`, etc. as needed. |
| `--depth` | unlimited | Maximum directory depth (0 = only files directly in `DIRECTORY`). |
| `--include` | all files | Filename glob (e.g. `*.py`). Matched against the filename, not the full path. |

### Example

```bash
parsetodo --tag TODO --depth 2 --include '*.py' src/
```

Prints each matching file's relative path followed by its TODO blocks, separated by `----------`.

## Library use

```python
from todo_comment_parser.parser import Parser

parser = Parser.from_file("some_file.py", todo_tag="TODO")
for block in parser.todo_pars:
    print(block)
```

`Parser.from_file` returns `None` if the file can't be read (binary file, permission error, etc.) and emits a warning.

## Behavior notes

- A TODO block ends at the first line that doesn't start with the same comment prefix as the TODO line. A new TODO encountered mid-block starts a new block.
- Comment prefix is detected as everything between the line's leading whitespace and the tag. Indentation is ignored when matching continuation lines, so an indented TODO can have indented continuations.
- Files containing TODOs with different comment prefixes (after stripping whitespace) raise `ValueError`.
