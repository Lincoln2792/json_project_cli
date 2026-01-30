# JSON Project CLI (create-json-project)

CLI em Python para **criar estruturas de pastas e arquivos** a partir de um arquivo **JSON**.  
Ideal para bootstrap de projetos (ex.: APIs, CLIs, microsserviços), padronização de scaffolding e criação rápida de templates.

---

## Visão geral

Com este comando, você consegue:

- Entrar no diretório desejado
- Apontar para um `estrutura.json` (no mesmo local ou caminho completo)
- Criar automaticamente toda a árvore do projeto: **pastas + arquivos + conteúdo inicial**

---

## Instalação
- Opção 1: Instalar em modo desenvolvimento (editável) — recomendado durante ajustes
pip install -e .

- Opção 2: Instalar normal
pip install .

- Verificar se o comando está disponívelpip install -e .
create-json-project --help

---

## Uso
Criar no diretório atual
create-json-project estrutura.json

Fallback:

python -m json_project_cli.cli estrutura.json

-Criar em um diretório específico
create-json-project estrutura.json --out "C:\Projetos"

-Sobrescrever arquivos existentes
create-json-project estrutura.json --overwrite

---

## Exemplo:
```powershell
cd "C:\Projetos"
create-json-project estrutura.json

Exemplo JSON
{
  "root": "meu_projeto",
  "folders": ["config", "src", "tests", { "name": "docs", "folders": ["imgs"] }],
  "files": [
    "README.md",
    ".gitignore",
    { "path": "src/main.py", "content": "print('Projeto criado via JSON!')\n" },
    { "path": "config/app.yml", "content": "runtime:\n  environment: dev\n" }
  ]
}
```

## Uninstall
```pip uninstall json-project-cli```
