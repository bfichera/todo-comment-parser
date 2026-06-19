# todo-comment-parser

Walk a directory tree and print every TODO-style comment block from every text file it finds.

A "TODO block" is the TODO line plus any immediately-following lines that share the same comment prefix. Files that mix more than one comment style (e.g. `# ` and `// ` TODOs in the same file) are ignored.

## Install

Clone this repository and then run:

```bash
pip install .
```

This installs the console script `parsetodo`.

## Usage

```bash
parsetodo [--tag TAG] [--depth N] [--include PATTERN] DIRECTORY
```

| Flag | Default | Description |
| --- | --- | --- |
| `DIRECTORY` | `.` | Root directory to walk. |
| `--tag` | `TODO` | Token that marks a comment block. Use `FIXME`, `XXX`, etc. as needed. |
| `--depth` | unlimited | Maximum directory depth (0 = only files directly in `DIRECTORY`). |
| `--include` | all files | Filename glob (e.g. `*.py`). |

### Example

```bash
parsetodo --tag TODO --depth 2 --include '*.py' src/
```
