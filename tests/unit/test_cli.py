from pathlib import Path

from aidd_forge.cli import build_parser, main


def test_build_parser_exposes_init_subcommand() -> None:
    parser = build_parser()
    args = parser.parse_args(["init", "some/path"])

    assert args.command == "init"
    assert args.path == "some/path"
    assert args.force is False


def test_init_default_path_is_current_dir() -> None:
    parser = build_parser()
    args = parser.parse_args(["init"])

    assert args.path == "."


def test_init_force_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["init", "--force"])

    assert args.force is True


def test_main_init_creates_governance_files(tmp_path: Path) -> None:
    exit_code = main(["init", str(tmp_path)])

    assert exit_code == 0
    assert (tmp_path / "governance" / "AGENTS.md").exists()
    assert (tmp_path / "CLAUDE.md").exists()


def test_main_init_is_idempotent_without_force(tmp_path: Path, capsys) -> None:
    main(["init", str(tmp_path)])
    capsys.readouterr()

    exit_code = main(["init", str(tmp_path)])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "arquivos criados: 0" in output
