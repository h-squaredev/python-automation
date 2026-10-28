"""Organiza uma cópia de trabalho por extensão. Execute --dry-run primeiro."""
import argparse
import shutil
from pathlib import Path


def organizar_arquivos(pasta_base, dry_run=False):
    pasta = Path(pasta_base).resolve()
    if not pasta.is_dir():
        raise ValueError("Pasta inexistente ou inválida.")
    # Fotografia inicial: nunca percorre destinos criados durante os movimentos.
    arquivos = sorted(p for p in pasta.rglob("*") if p.is_file() and not p.is_symlink())
    reservados = set(arquivos)
    movimentos = []
    for arquivo in arquivos:
        extensao = arquivo.suffix.lower().lstrip(".")
        if not extensao:
            continue
        destino_pasta = pasta / extensao
        if arquivo.parent == destino_pasta:
            continue
        if destino_pasta.exists() and (destino_pasta.is_symlink() or not destino_pasta.is_dir()):
            raise ValueError(f"Destino não é uma pasta segura: {destino_pasta.name}")
        destino = destino_pasta / arquivo.name
        contador = 1
        while destino in reservados or destino.exists():
            destino = destino_pasta / f"{arquivo.stem}_{contador}{arquivo.suffix}"
            contador += 1
        reservados.add(destino)
        movimentos.append((arquivo, destino))
    for origem, destino in movimentos:
        print(f"{origem.relative_to(pasta)} -> {destino.relative_to(pasta)}")
        if not dry_run:
            destino.parent.mkdir(exist_ok=True)
            # Nunca substitui um arquivo criado depois do planejamento.
            if destino.exists():
                raise FileExistsError(f"Destino já existe: {destino.name}")
            shutil.move(str(origem), str(destino))
    print(f"{'Planejados' if dry_run else 'Movidos'}: {len(movimentos)} arquivo(s).")
    return movimentos


def main():
    parser = argparse.ArgumentParser(description="Agrupa arquivos por extensão, sem apagar pastas.")
    parser.add_argument("pasta", type=Path)
    parser.add_argument("--dry-run", action="store_true", help="Mostra o plano sem mover arquivos.")
    args = parser.parse_args()
    try:
        organizar_arquivos(args.pasta, args.dry_run)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Erro: {exc}\n")


if __name__ == "__main__":
    main()
