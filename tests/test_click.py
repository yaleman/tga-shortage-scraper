"""testing click functionality"""

from click.testing import CliRunner
from tga_shortage_scraper.__main__ import main


def test_command_help() -> None:
    """test that something works using click"""
    runner = CliRunner()
    result = runner.invoke(
        main,
        ["--help"],
    )
    assert result.exit_code == 0
    print(result)


def test_actual_command() -> None:
    """test that something works using click"""
    runner = CliRunner()
    result = runner.invoke(
        main,
        [],
    )
    assert result.exit_code == 0
    print(result)
