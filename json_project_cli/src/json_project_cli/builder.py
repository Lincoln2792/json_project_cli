from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Union


Json = Dict[str, Any]
FolderSpec = Union[str, Dict[str, Any]]
FileSpec = Union[str, Dict[str, Any]]


@dataclass
class BuildOptions:
    dry_run: bool = False
    overwrite_files: bool = False
    verbose: bool = True


def _log(msg: str, opt: BuildOptions) -> None:
    if opt.verbose:
        print(msg)


def _safe_join(base: Path, rel: str) -> Path:
    # evita "../" sair do root
    rel_path = Path(rel)
    target = (base / rel_path).resolve()
    base_resolved = base.resolve()
    if base_resolved != target and base_resolved not in target.parents:
        raise ValueError(f"Caminho inválido fora do root: {rel}")
    return target


def _ensure_dir(path: Path, opt: BuildOptions) -> None:
    if opt.dry_run:
        _log(f"[DRY] mkdir -p {path}", opt)
        return
    path.mkdir(parents=True, exist_ok=True)
    _log(f"[OK] pasta: {path}", opt)


def _write_file(path: Path, content: str, opt: BuildOptions) -> None:
    if path.exists() and not opt.overwrite_files:
        _log(f"[SKIP] arquivo já existe: {path}", opt)
        return

    if opt.dry_run:
        _log(f"[DRY] write {path} ({len(content)} chars)", opt)
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _log(f"[OK] arquivo: {path}", opt)


def _build_folders(root: Path, folders: List[FolderSpec], opt: BuildOptions) -> None:
    for item in folders:
        if isinstance(item, str):
            _ensure_dir(_safe_join(root, item), opt)
        elif isinstance(item, dict):
            name = item.get("name")
            if not name or not isinstance(name, str):
                raise ValueError(f"Pasta com 'name' inválido: {item}")
            base = _safe_join(root, name)
            _ensure_dir(base, opt)

            sub = item.get("folders", [])
            if sub:
                if not isinstance(sub, list):
                    raise ValueError(f"'folders' deve ser lista em: {item}")
                _build_folders(base, sub, opt)
        else:
            raise ValueError(f"Tipo de pasta inválido: {type(item)}")


def _build_files(root: Path, files: List[FileSpec], opt: BuildOptions) -> None:
    for item in files:
        if isinstance(item, str):
            path = _safe_join(root, item)
            _write_file(path, "", opt)
        elif isinstance(item, dict):
            rel = item.get("path")
            if not rel or not isinstance(rel, str):
                raise ValueError(f"Arquivo com 'path' inválido: {item}")
            content = item.get("content", "")
            if content is None:
                content = ""
            if not isinstance(content, str):
                raise ValueError(f"'content' deve ser string em: {item}")
            path = _safe_join(root, rel)
            _write_file(path, content, opt)
        else:
            raise ValueError(f"Tipo de arquivo inválido: {type(item)}")


def build_from_json(json_data: Json, output_dir: Path, opt: BuildOptions) -> Path:
    root_name = json_data.get("root")
    if not root_name or not isinstance(root_name, str):
        raise ValueError("JSON precisa ter 'root' (string).")

    root_path = (output_dir / root_name).resolve()
    _ensure_dir(root_path, opt)

    folders = json_data.get("folders", [])
    if folders:
        if not isinstance(folders, list):
            raise ValueError("'folders' deve ser uma lista.")
        _build_folders(root_path, folders, opt)

    files = json_data.get("files", [])
    if files:
        if not isinstance(files, list):
            raise ValueError("'files' deve ser uma lista.")
        _build_files(root_path, files, opt)

    return root_path
