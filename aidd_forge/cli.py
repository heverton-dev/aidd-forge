"""Entrypoint CLI do AIDD Forge.

Uso:
    forge init [path] [--force]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aidd_forge.core.injector import Injector

TEMPLATES_ROOT = Path(__file__).parent / "templates"

IDE_RULE_ALIASES = {
    "CLAUDE.md": "governance/AGENTS.md",
}


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    injector = Injector(TEMPLATES_ROOT, target, force=args.force)
    files_result = injector.run()
    links_result = injector.link_ide_rules(IDE_RULE_ALIASES)

    print(f"[aidd-forge] projeto alvo: {target}")
    print(f"[aidd-forge] arquivos criados: {len(files_result.created)}")
    print(f"[aidd-forge] arquivos ignorados (ja existem): {len(files_result.skipped)}")
    if files_result.overwritten:
        print(f"[aidd-forge] arquivos sobrescritos: {len(files_result.overwritten)}")
    print(f"[aidd-forge] regras de IDE vinculadas: {len(links_result.created)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="AIDD Forge - motor de governanca agentica e economia de tokens",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="Injeta a infraestrutura AIDD no projeto alvo"
    )
    init_parser.add_argument(
        "path", nargs="?", default=".", help="Caminho do projeto alvo (padrao: diretorio atual)"
    )
    init_parser.add_argument(
        "--force", action="store_true", help="Sobrescreve arquivos ja existentes no alvo"
    )
    init_parser.set_defaults(func=cmd_init)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
