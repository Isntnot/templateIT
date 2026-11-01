# TemplateIT

A small command-line tool that creates new files from templates. It acts as a substitute for the Obsidian formatter/Templater workflow, so you can create a file from the terminal and have the right template applied based on the folder it lives in.

## Features

- Picks a template automatically based on the folder of the file you are creating.
- Finds the config file (`template.txt`) by walking up the parent directories.
- Supports a subset of Obsidian Templater expressions (`tp.file.title`, `tp.date.now`).
- Supports Moment.js-style date formats (`YYYY-MM-DD`, `dddd`, `MMMM`, ...).
- Refuses to overwrite files that already exist.

## Requirements

- Python 3.9+ (uses `Path.is_relative_to` and built-in generic type hints)
- No third-party dependencies

## Usage

```bash
python main.py path/to/new_note.md
```

TemplateIT will:

1. Look for a `template.txt` in the current directory, then in its parent, then in the grandparent (3 levels in total, see `MAX_DEEP` in `main.py`).
2. Read the folder-to-template mapping from it.
3. Find the first folder that contains the target file and load its template.
4. Process the template expressions and write the result to the new file.

If no `template.txt` is found, or no folder matches the target file, the program exits with a `FileNotFoundError`.

### Options

| Option | Description |
| --- | --- |
| `filename` | Path of the file to create (required). |
| `-s`, `--substitute` | Declared in the argument parser, but not wired up yet (see Limitations). |

## The `template.txt` file

Each line maps a folder to a template file, separated by `=`:

```
# folder = template
daily   = templates/daily.md
notes/projects = templates/project.md
/absolute/path/to/journal = /absolute/path/to/templates/journal.md
```

Rules:

- Blank lines and lines starting with `#` are ignored.
- The line is split on the first `=`; whitespace around both parts is trimmed.
- Relative paths are resolved against the folder where `template.txt` lives, not the current working directory.
- Absolute paths are used as they are.
- A file can match a folder at any depth below it. When several lines match, the first one in the file wins, so put the most specific folders first.
- A folder entry that points to an existing file, or a template entry that points to an existing folder, raises an error.

### Example

Project layout:

```
vault/
├── template.txt
├── templates/
│   ├── daily.md
│   └── project.md
├── daily/
└── projects/
```

`vault/template.txt`:

```
daily = templates/daily.md
projects = templates/project.md
```

Create a new daily note:

```bash
cd vault/daily
python /path/to/TemplateIT/main.py 2026-11-01.md
```

## Template syntax

| Expression | Result |
| --- | --- |
| `<% tp.file.title %>` | The name of the file being created (including its extension). |
| `<% tp.date.now() %>` | Today's date as `YYYY-MM-DD`. |
| `<% tp.date.now("FORMAT") %>` | Today's date in the given format. |
| `<% tp.date.now("FORMAT", N) %>` | The date `N` days from today (negative values go back). |

Example template:

```markdown
---
title: <% tp.file.title %>
date: <% tp.date.now("YYYY-MM-DD") %>
next_week: <% tp.date.now("YYYY-MM-DD", 7) %>
---
# <% tp.file.title %>
Hello! Today is <% tp.date.now("dddd, MMMM Do YYYY") %>.
```

### Supported date tokens

| Moment.js | Meaning | Python |
| --- | --- | --- |
| `YYYY`, `YY` | Year | `%Y`, `%y` |
| `MMMM`, `MMM`, `MM` | Month (full name, short name, number) | `%B`, `%b`, `%m` |
| `DD`, `D` | Day of month | `%d` |
| `dddd`, `ddd` | Weekday (full, short) | `%A`, `%a` |
| `HH`, `mm`, `ss` | Hour (24h), minutes, seconds | `%H`, `%M`, `%S` |
| `A` | AM/PM | `%p` |
| `Do` | Day of month (no ordinal suffix) | `%d` |

Month and weekday names follow the system locale.

## Project structure

```
.
├── main.py              # Entry point: finds config, matches template, creates file
├── argprs.py            # Command-line argument parser
├── tps.py               # Locates and parses template.txt
└── utils/
    ├── creation.py      # Safe file creation
    ├── dirmatching.py   # Checks whether a file is inside a directory
    └── templater.py     # Templater expressions and Moment.js format conversion
```

## Limitations

- `--substitute` is parsed but not passed to `createFile`, so existing files are never overwritten.
- `tp.file.title` currently returns the file name with its extension, not just the title.
- `Do` does not add ordinal suffixes (1st, 2nd, ...); it prints the plain day number.
- Only `tp.file.title` and `tp.date.now` are implemented; other Templater functions are left untouched in the output.
- Config lookup is limited to 3 directory levels.
- The new file's parent folder must already exist.
