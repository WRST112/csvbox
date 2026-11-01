import argparse
import csv
import sys


def read_csv(path):
    """Read a CSV file and pad or trim every row to the header width."""
    # newline="" is required by csv, otherwise quoted line breaks break parsing
    with open(path, encoding="utf-8", newline="") as file:
        rows = [row for row in csv.reader(file) if row]

    if not rows:
        return []

    column_count = len(rows[0])
    for index in range(1, len(rows)):
        if len(rows[index]) > column_count:
            message = "Warning: row " + str(index + 1) + " has extra columns, dropped"
            print(message, file=sys.stderr)
        rows[index] = rows[index][:column_count] + [""] * (column_count - len(rows[index]))

    return rows


def rule(left, middle, right, widths):
    """Build a horizontal border from the given corner and joint characters."""
    return left + middle.join("─" * (width + 2) for width in widths) + right


def row_line(cells, widths):
    """Format one row with padding and vertical borders."""
    return "│ " + " │ ".join(cell.ljust(width) for cell, width in zip(cells, widths)) + " │"


def to_table(rows):
    """Render rows as a box-drawn table sized to the widest cell."""
    header, body = rows[0], rows[1:]
    widths = [max(len(row[column]) for row in rows) for column in range(len(header))]

    lines = [rule("┌", "┬", "┐", widths), row_line(header, widths)]
    if body:
        lines.append(rule("├", "┼", "┤", widths))
    for row in body:
        lines.append(row_line(row, widths))
    lines.append(rule("└", "┴", "┘", widths))

    return "\n".join(lines)


def main():
    """Print the box-drawn table for the CSV file passed on the command line."""
    parser = argparse.ArgumentParser(description="Print a CSV file as a box-drawn table.")
    parser.add_argument("path", help="path to the CSV file")
    args = parser.parse_args()

    try:
        rows = read_csv(args.path)
    except FileNotFoundError:
        sys.exit("Error: file not found: " + args.path)
    except UnicodeDecodeError:
        sys.exit("Error: file is not valid UTF-8: " + args.path)
    except csv.Error as error:
        sys.exit("Error in CSV file: " + str(error))
    except OSError:
        sys.exit("Error: cannot read file: " + args.path)

    if not rows:
        sys.exit("Error: file is empty: " + args.path)

    print(to_table(rows))


if __name__ == "__main__":
    main()
