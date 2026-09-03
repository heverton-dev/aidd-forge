# Manual Prático de Uso e Operação: AIDD Forge

> **Versão:** 1.0.0  
> **Para quem é este manual:** Desenvolvedores, tech leads e operadores de agentes que utilizam o AIDD Forge no dia a dia.

---

## 1. Comandos da CLI

O ponto de entrada formal da CLI é o comando `forge` (ou `python -m aidd_forge.cli`):

### `forge init [caminho] [--force]`
Inicializa a estrutura de governança no projeto alvo.
- `[caminho]` *(opcional)*: Diretório onde a infraestrutura será injetada (padrão: diretório atual `.`).
- `--force` *(opcional)*: Sobrescreve arquivos pré-existentes, restaurando as versões oficiais dos templates.

**Exemplo:**
```bash
# Injeta no projeto atual
forge init

# Injeta em um subdiretório específico
forge init ../meu-novo-microsservico

# Restaura regras padrão sobrescrevendo alterações
forge init --force
```

---

## 2. Estrutura de Pastas Injetada no Projeto

Após a execução do `forge init`, o projeto de destino recebe a seguinte infraestrutura:

```text
meu-projeto/
├── .aidd/
│   └── pipeline/                      # Micro-ambientes granulares por fase
│       ├── phase_00_bootstrap/        # AGENTS.md + mcp_config.json
│       ├── phase_01_requirements/     # AGENTS.md + mcp_config.json
│       ├── phase_02_architecture/     # AGENTS.md + mcp_config.json
│       ├── phase_03_implementation/   # AGENTS.md + mcp_config.json
│       └── phase_04_audit_security/   # AGENTS.md + mcp_config.json
├── .agent/
│   ├── commands/                      # Slash commands universais
│   └── skills/                        # As 6 skills oficiais injetadas
├── .claude/
│   └── commands/                      # Comandos para Claude Code
├── .cursor/
│   └── rules/                         # Regras de disparo para Cursor IDE
├── .git/
│   └── hooks/
│       └── pre-commit                 # Bloqueio binário dos 7 Gates
├── governance/
│   └── AGENTS.md                      # Carta canônica de regras
├── CLAUDE.md                          # Alias automático para AGENTS.md
├── setup.bat                          # Executável de 1-clique (Windows)
└── setup.sh                           # Executável de 1-clique (Linux/Mac)
```

---

## 3. As 6 Skills Especializadas Disponíveis

Cada skill pode ser invocada ou referenciada pelos agentes durante o desenvolvimento:

1. **`caveman-ultra`**: Ativação do modo de máxima densidade de tokens (In: EN, CoT: Caveman, Out: PT-BR).
2. **`orca-orchestration`**: Roteamento multi-agente, trabalho em branches separadas e decision gates.
3. **`impeccable-ui`**: Criação de interfaces modernas Tailwind sem elementos infantis/emojis.
4. **`open-code-review`**: Auditoria arquitetural de acoplamento e Clean Architecture.
5. **`post-mortem`**: Relatório de análise de incidentes baseado nos 5-Porquês.
6. **`cybersecurity-audit`**: Varredura de vulnerabilidades de segurança OWASP Top 10.

---

## 4. Guia de Solução de Problemas (Troubleshooting)

### Q1: O comando `forge` não é reconhecido no terminal.
- **Causa:** O pacote ainda não foi instalado no ambiente Python ativo.
- **Solução:** Execute `pip install -e .` na raiz do repositório `aidd-forge` ou use `python -m aidd_forge.cli init`.

### Q2: O `pre-commit` bloqueou meu commit informando falha no `G_BLOQUEAR_SEGREDOS`.
- **Causa:** Um arquivo recém-adicionado contém uma chave de API, senha real ou padrão correspondente a segredos.
- **Solução:** Remova o segredo do código e utilize variáveis de ambiente (`.env`).

### Q3: Tenho apenas um agente instalado (ex: Cursor). O ORCA vai quebrar?
- **Causa:** Não.
- **Solução:** O `detector.py` e `orca_bridge.py` geram automaticamente o modo `single_agent_isolated`, permitindo que todos os papéis operem isolados no mesmo agente sem falha.
