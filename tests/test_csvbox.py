import sys

import pytest

import csvbox


def write_csv(tmp_path, text, encoding="utf-8"):
    """Write text to a CSV file and return its path."""
    path = tmp_path / "data.csv"
    path.write_text(text, encoding=encoding)
    return str(path)


def run_main(monkeypatch, path):
    """Run main with a single argument and return the SystemExit."""
    monkeypatch.setattr(sys, "argv", ["csvbox", path])
    with pytest.raises(SystemExit) as exit_info:
        csvbox.main()
    return exit_info.value


def test_table_matches_spec(tmp_path):
    path = write_csv(tmp_path, "Имя,Возраст,Город\nАлиса,30,Москва\nБоб,25,СПб\n")
    table = csvbox.to_table(csvbox.read_csv(path))
    assert table == (
        "┌───────┬─────────┬────────┐\n"
        "│ Имя   │ Возраст │ Город  │\n"
        "├───────┼─────────┼────────┤\n"
        "│ Алиса │ 30      │ Москва │\n"
        "│ Боб   │ 25      │ СПб    │\n"
        "└───────┴─────────┴────────┘"
    )


def test_header_only(tmp_path):
    path = write_csv(tmp_path, "a,b\n")
    assert csvbox.to_table(csvbox.read_csv(path)) == (
        "┌───┬───┐\n"
        "│ a │ b │\n"
        "└───┴───┘"
    )


def test_short_row_is_padded(tmp_path):
    rows = csvbox.read_csv(write_csv(tmp_path, "a,b,c\n1,2\n"))
    assert rows == [["a", "b", "c"], ["1", "2", ""]]


def test_long_row_is_truncated(tmp_path, capsys):
    rows = csvbox.read_csv(write_csv(tmp_path, "a,b\n1,2,3\n"))
    assert rows == [["a", "b"], ["1", "2"]]
    assert "extra columns" in capsys.readouterr().err


def test_blank_lines_are_skipped(tmp_path):
    rows = csvbox.read_csv(write_csv(tmp_path, "a,b\n\n1,2\n"))
    assert rows == [["a", "b"], ["1", "2"]]


def test_main_prints_table(tmp_path, monkeypatch, capsys):
    path = write_csv(tmp_path, "a,b\n1,2\n")
    monkeypatch.setattr(sys, "argv", ["csvbox", path])
    csvbox.main()
    assert capsys.readouterr().out == (
        "┌───┬───┐\n"
        "│ a │ b │\n"
        "├───┼───┤\n"
        "│ 1 │ 2 │\n"
        "└───┴───┘\n"
    )


def test_missing_file(tmp_path, monkeypatch):
    exit_info = run_main(monkeypatch, str(tmp_path / "nope.csv"))
    assert "file not found" in str(exit_info.code)


def test_empty_file(tmp_path, monkeypatch):
    exit_info = run_main(monkeypatch, write_csv(tmp_path, ""))
    assert "file is empty" in str(exit_info.code)


def test_wrong_encoding(tmp_path, monkeypatch):
    path = write_csv(tmp_path, "Имя,Город\nАлиса,Москва\n", encoding="cp1251")
    exit_info = run_main(monkeypatch, path)
    assert "not valid UTF-8" in str(exit_info.code)


def test_no_arguments(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["csvbox"])
    with pytest.raises(SystemExit) as exit_info:
        csvbox.main()
    assert exit_info.value.code == 2
    assert "required" in capsys.readouterr().err
