from __future__ import annotations

import json
from pathlib import Path
import argparse

from .builder import BuildOptions, build_from_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="create-json-project",
        description="Cria estrutura de projeto (pastas/arquivos) a partir de um JSON.",
    )
    parser.add_argument(
        "json_file",
        help="Arquivo JSON (pode ser só o nome se estiver no mesmo diretório). Ex: estrutura.json",
    )
    parser.add_argument(
        "--out",
        default=".",
        help="Pasta onde criar o projeto (padrão: diretório atual).",
    )
    parser.add_argument("--dry", action="store_true", help="Simula sem criar nada.")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescreve arquivos existentes.")
    parser.add_argument("--quiet", action="store_true", help="Menos logs.")

    args = parser.parse_args()

    json_path = Path(args.json_file).resolve()
    if not json_path.exists():
        raise SystemExit(f"JSON não encontrado: {json_path}")

    data = json.loads(json_path.read_text(encoding="utf-8"))
    opt = BuildOptions(
        dry_run=args.dry,
        overwrite_files=args.overwrite,
        verbose=not args.quiet,
    )

    created_root = build_from_json(data, Path(args.out), opt)
    if opt.verbose:
        print(f"\nRaiz criada: {created_root}")
