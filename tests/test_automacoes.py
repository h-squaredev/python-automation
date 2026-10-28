"""Testes sem documentos reais ou alteração de dados fora de pasta temporária."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

organizador = load("organizador", "OrganizarArquivos/organizador_de_arquivo_1.py")
renomeador = load("renomeador", "RenomearPDFs/renomear_pdfs.py")

class OrganizadorTests(unittest.TestCase):
    def test_dry_run_e_segunda_execucao(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "origem").mkdir()
            arquivo = base / "origem" / "exemplo.pdf"
            arquivo.write_text("fictício")
            organizador.organizar_arquivos(base, dry_run=True)
            self.assertTrue(arquivo.exists())
            organizador.organizar_arquivos(base)
            self.assertTrue((base / "pdf" / "exemplo.pdf").exists())
            self.assertEqual(organizador.organizar_arquivos(base), [])

    def test_colisao_preserva_conteudo(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            (base / "pdf").mkdir()
            (base / "pdf" / "exemplo.pdf").write_text("antigo")
            (base / "exemplo.pdf").write_text("novo")
            organizador.organizar_arquivos(base)
            self.assertEqual((base / "pdf" / "exemplo.pdf").read_text(), "antigo")
            self.assertEqual((base / "pdf" / "exemplo_1.pdf").read_text(), "novo")

class RenomeadorTests(unittest.TestCase):
    def test_dry_run_e_colisao(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            arquivo = base / "entrada.PDF"
            arquivo.write_text("fictício")
            destino = base / "0000_FORNECEDOR_FICTICIO.pdf"
            destino.write_text("preservar")
            with patch.object(renomeador, "find_processo_fornecedor", return_value=("0000", "FORNECEDOR FICTICIO")):
                renomeador.rename_pdfs(base, dry_run=True)
                self.assertTrue(arquivo.exists())
                renomeador.rename_pdfs(base)
            self.assertEqual(destino.read_text(), "preservar")
            self.assertEqual((base / "0000_FORNECEDOR_FICTICIO_2.pdf").read_text(), "fictício")

    def test_extracao_de_pdf_ficticio(self):
        from pypdf import PdfWriter
        from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject
        with tempfile.TemporaryDirectory() as tmp:
            arquivo = Path(tmp) / "ficticio.pdf"
            writer = PdfWriter()
            page = writer.add_blank_page(width=612, height=792)
            font = DictionaryObject({NameObject("/Type"): NameObject("/Font"), NameObject("/Subtype"): NameObject("/Type1"), NameObject("/BaseFont"): NameObject("/Helvetica")})
            page[NameObject("/Resources")] = DictionaryObject({NameObject("/Font"): DictionaryObject({NameObject("/F1"): writer._add_object(font)})})
            stream = DecodedStreamObject()
            stream.set_data(b"BT /F1 12 Tf 50 750 Td (PROCESSO: 0000) Tj 0 -20 Td (Devera ser pago a: FORNECEDOR FICTICIO) Tj ET")
            page[NameObject("/Contents")] = writer._add_object(stream)
            with arquivo.open("wb") as output:
                writer.write(output)
            self.assertEqual(renomeador.find_processo_fornecedor(arquivo), ("0000", "FORNECEDOR FICTICIO"))

if __name__ == "__main__":
    unittest.main()
