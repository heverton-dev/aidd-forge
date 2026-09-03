# AGENTS.md — Regras de Operação no Repositório AIDD Forge

> **Projeto:** `AIDD Forge`  
> **Papel do Arquivo:** Governança Canônica e Instruções Primárias para qualquer Agente de IA operando nesta base.

---

## 1. Tríade Caveman Ultra (Mandatória)

Para máxima economia de tokens e precisão técnica:
1. **ENTRADA (Rules/System Prompts):** Arquivos de regras e comandos em Inglês enxuto.
2. **PROCESSAMENTO (Internal CoT / Thinking):** Estilo English Caveman telegráfico (3 a 5 linhas, sem artigos e sem preposições desnecessárias).
3. **SAÍDA (Comunicação e Código):** Respostas, relatórios, commits e código estritamente em **Português do Brasil (PT-BR)** de alta densidade técnica.

---

## 2. Padrões Arquiteturais Rígidos

- **Zero Stubs:** É proibido commitar métodos vazios (`pass`), retornos fictícios ou mocks de fachada em código de produção.
- **Result Monad:** Todo serviço ou rotina suscetível a erro operacional deve retornar `Result.ok(valor)` ou `Result.fail(erro)`.
- **Descarte de Contexto (Context-Purge):** Subagentes cognitivos devem receber apenas a especificação atômica da tarefa e ser finalizados imediatamente após salvar o artefato e validar via AST.
- **7 Quality Gates:** Toda alteração deve passar pelos 7 gates determinísticos presentes em `aidd_forge/templates/gates/`.

---

## 3. Disparo por Linguagem Natural e Comandos

- `/forge` ou `/aidd-init`: Executa o bootstrap determinístico via `python -m aidd_forge.cli init`.
- Linguagem Natural: Intenções como *"prepare o ambiente"*, *"configure com aidd"* ou *"blinde as regras"* disparam a rotina de injeção automática.

---

## 4. Agnosticismo de Harness

Este repositório suporta e reconhece qualquer harness ativo:
- **Antigravity / Open Code / MimoCode:** Leem `.agent/` e as diretivas deste `AGENTS.md`.
- **Claude Code:** Lê `CLAUDE.md` (vinculado a este arquivo) e `.claude/commands/`.
- **Cursor:** Lê `.cursor/rules/`.
