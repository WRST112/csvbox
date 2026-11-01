# csvbox

CSV files look like noise in a terminal. `csvbox` turns them into a proper table:

```
$ csvbox examples/data.csv
┌───────┬─────┬──────────────────┐
│ Name  │ Age │ City             │
├───────┼─────┼──────────────────┤
│ Alice │ 30  │ Moscow           │
│ Bob   │ 25  │ Saint Petersburg │
└───────┴─────┴──────────────────┘
```

## Install

Python 3.8 or newer.

```bash
pip install csvbox
```

This adds the `csvbox` command:

```bash
csvbox examples/data.csv
```

Or skip installing entirely and run it from the source tree:

```bash
python csvbox.py examples/data.csv
```

## Usage

The table goes to stdout, so it can be piped or saved:

```bash
csvbox examples/data.csv > table.txt
```

How it behaves:

- the first CSV row becomes the header, separated by a rule;
- every column is as wide as its longest value;
- short rows are padded with empty cells, long rows are cut and reported on stderr;
- files are read as UTF-8, so Cyrillic and other non-ASCII text works;
- a header-only file is drawn without the middle rule.

## Errors

No tracebacks: one readable message and exit code 1.

| Case                | Message                                    |
|---------------------|--------------------------------------------|
| file does not exist | `Error: file not found: data.csv`          |
| file is empty       | `Error: file is empty: data.csv`           |
| file is not UTF-8   | `Error: file is not valid UTF-8: data.csv` |
| file cannot be read | `Error: cannot read file: data.csv`        |

Running the script without a path prints the usual argparse usage hint. That is expected behaviour, not a converter error.

## Limitations

- **BOM.** CSV files saved by Excel as "CSV UTF-8" start with a byte order mark, and the first header keeps an invisible `\ufeff`. If you need those, change `encoding="utf-8"` to `encoding="utf-8-sig"` in `read_csv`.
- **`|` inside a cell** is printed as is: this is a terminal table, not Markdown.
- **Box drawing on Windows.** Output is Unicode. Redirecting to a file from a legacy console may need `PYTHONIOENCODING=utf-8`.

## Development

```bash
pip install pytest
pytest
```

Layout:

```
csvbox.py              # all the code: read_csv, rule, row_line, to_table, main
tests/test_csvbox.py   # tests
examples/              # sample inputs
```

## License

MIT — see [LICENSE](LICENSE).
