"""Entrypoint CLI do AIDD Forge.

Uso:
    forge init [path] [--force]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from aidd_forge.commands.slash_router import SlashRouter
from aidd_forge.core.git_hooks import GitHooksInstaller
from aidd_forge.core.injector import Injector
from aidd_forge.core.phase_fencer import PhaseFencer

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
    skills_result = injector.link_skills()

    fencer = PhaseFencer(TEMPLATES_ROOT, target, force=args.force)
    fence_result = fencer.run()

    router = SlashRouter(target, force=args.force)
    router_result = router.run()

    hooks = GitHooksInstaller(TEMPLATES_ROOT, target, force=args.force)
    hooks_result = hooks.run()

    print(f"[aidd-forge] projeto alvo: {target}")
    print(f"[aidd-forge] arquivos criados: {len(files_result.created)}")
    print(f"[aidd-forge] arquivos ignorados (ja existem): {len(files_result.skipped)}")
    if files_result.overwritten:
        print(f"[aidd-forge] arquivos sobrescritos: {len(files_result.overwritten)}")
    print(f"[aidd-forge] regras de IDE vinculadas: {len(links_result.created)}")
    print(f"[aidd-forge] skills vinculadas em .agent/skills/: {len(skills_result.created)}")
    print(f"[aidd-forge] fases provisionadas: {len(fence_result.phases)}")
    print(f"[aidd-forge] slash commands gravados: {len(router_result.created)}")
    if router_result.intent_router_injected:
        print("[aidd-forge] Intent Router injetado no AGENTS.md existente")
    print(f"[aidd-forge] quality gates instalados: {len(hooks_result.gate_scripts)}")
    if hooks_result.hook_installed:
        print(f"[aidd-forge] hook pre-commit instalado em: {hooks_result.hook_path}")
    elif hooks_result.skipped_reason:
        print(f"[aidd-forge] hook pre-commit nao instalado: {hooks_result.skipped_reason}")
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
