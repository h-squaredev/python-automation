#!/usr/bin/env python3
"""
Renomeia PDFs de Ordens de Pagamento com base no número do PROCESSO e no
Fornecedor ("Deverá ser pago a:"), extraídos da página que contém esses
dados. Normalmente essa página é a 2ª (Ordem de Pagamento); se faltar o
comprovante de transferência no início do PDF, ela passa a ser a 1ª — o
script procura em ambas automaticamente.

Padrão de nome gerado (exemplo fictício):
    {processo}_{fornecedor com cada caractere não alfanumérico -> "_"}.pdf
    ex.: "0000_FORNECEDOR_FICTICIO.pdf"

USO:
    python3 renomear_pdfs.py /caminho/da/pasta            # renomeia de verdade
    python3 renomear_pdfs.py /caminho/da/pasta --dry-run  # só mostra o preview

REQUISITOS:
    pip install pdfplumber pytesseract pypdf

    Os PDFs deste tipo costumam ser digitalizados (sem texto selecionável),
    então o script usa OCR (Tesseract) como fallback automático:
        sudo apt-get install tesseract-ocr tesseract-ocr-por
    (o pacote "tesseract-ocr-por" dá muito mais precisão em campos com
    acento, como "Deverá"; sem ele o script ainda tenta com o idioma
    padrão instalado, mas pode errar acentos).
"""
import argparse
import re
import sys
import os
import shutil
from pathlib import Path

import pdfplumber

try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    pytesseract = None

# Usa PATH por padrão; permite configurar outra instalação sem editar o código.
if OCR_AVAILABLE and os.environ.get("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = os.environ["TESSERACT_CMD"]


PROCESSO_RE = re.compile(r'PROCESSO[:\s]*([0-9]+)', re.IGNORECASE)
FORNECEDOR_RE = re.compile(r'Dever[aá]\s+ser\s+pago\s+a[:\s]*(.+)', re.IGNORECASE)

# a Ordem de Pagamento normalmente está na 1ª ou 2ª página do PDF
MAX_PAGES_TO_CHECK = 2


def extract_page_text(page) -> str:
    """Extrai texto normal da página; se vier vazio (PDF escaneado), usa OCR."""
    text = page.extract_text() or ""
    if text.strip():
        return text

    if not OCR_AVAILABLE:
        return ""

    image = page.to_image(resolution=300).original
    try:
        return pytesseract.image_to_string(image, lang="por")
    except Exception:
        # pacote de idioma "por" não instalado no tesseract: tenta o padrão
        try:
            return pytesseract.image_to_string(image)
        except Exception:
            return ""


def find_processo_fornecedor(pdf_path: Path):
    """Procura Processo e Fornecedor nas primeiras páginas do PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:MAX_PAGES_TO_CHECK]:
            text = extract_page_text(page)
            proc_match = PROCESSO_RE.search(text)
            forn_match = FORNECEDOR_RE.search(text)
            if proc_match and forn_match:
                processo = proc_match.group(1).strip()
                fornecedor = forn_match.group(1)
                # corta na quebra de linha (ou antes de "CNPJ", por segurança)
                fornecedor = re.split(r'\n|CNPJ', fornecedor)[0].strip()
                return processo, fornecedor
    return None, None


def sanitize(name: str) -> str:
    """Troca cada caractere não alfanumérico por '_' (sem colapsar sequências)."""
    return re.sub(r'[^0-9A-Za-z]', '_', name).strip('_')


def rename_pdfs(folder: Path, dry_run: bool = False):
    pdf_files = sorted(p for p in folder.iterdir() if p.is_file() and not p.is_symlink() and p.suffix.lower() == ".pdf")
    if not pdf_files:
        print(f"Nenhum PDF encontrado em: {folder}")
        return

    used_names = {p.name.casefold() for p in folder.iterdir()}

    for pdf_path in pdf_files:
        try:
            processo, fornecedor = find_processo_fornecedor(pdf_path)
        except Exception as exc:
            print(f"[ERRO] {pdf_path.name}: falha ao ler o PDF ({exc})")
            continue

        if not processo or not fornecedor:
            print(f"[AVISO] Não encontrei Processo/Fornecedor em: {pdf_path.name} (deixei como está)")
            continue

        new_name = f"{processo}_{sanitize(fornecedor)}.pdf"

        # evita sobrescrever caso o nome já exista (soma sufixo _2, _3...)
        candidate = new_name
        counter = 2
        while candidate.casefold() in used_names and candidate != pdf_path.name:
            candidate = f"{processo}_{sanitize(fornecedor)}_{counter}.pdf"
            counter += 1
        new_name = candidate

        if new_name == pdf_path.name:
            print(f"[OK] Já está correto: {pdf_path.name}")
            continue

        used_names.discard(pdf_path.name.casefold())
        used_names.add(new_name.casefold())
        new_path = pdf_path.with_name(new_name)

        print(f"{pdf_path.name}  ->  {new_name}")
        if not dry_run:
            # Link exclusivo: falha se o destino existir, em vez de sobrescrever.
            try:
                os.link(pdf_path, new_path)
                pdf_path.unlink()
            except OSError as exc:
                print(f"[ERRO] Não foi possível renomear {pdf_path.name}: {exc}")


def main():
    parser = argparse.ArgumentParser(
        description="Renomeia PDFs de Ordens de Pagamento por Processo/Fornecedor."
    )
    parser.add_argument("pasta", help="Pasta contendo os PDFs a renomear")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostra os novos nomes, sem renomear de verdade",
    )
    args = parser.parse_args()

    folder = Path(args.pasta)
    if not folder.is_dir():
        print(f"Pasta não encontrada: {folder}")
        sys.exit(1)

    if not OCR_AVAILABLE:
        print("[AVISO] pytesseract não instalado: apenas PDFs com texto serão lidos.")
    elif not shutil.which(pytesseract.pytesseract.tesseract_cmd):
        print("[AVISO] Tesseract não encontrado. Instale-o ou configure TESSERACT_CMD para OCR.")
    rename_pdfs(folder, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
