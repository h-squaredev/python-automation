# Renomeador de PDFs

Lê as duas primeiras páginas de cada PDF da pasta, procura `PROCESSO:` e `Deverá ser pago a:` e gera nomes como `0000_FORNECEDOR_FICTICIO.pdf`. Este exemplo é fictício. Não percorre subpastas.

## Instalação

```sh
python -m pip install pdfplumber pytesseract
```

Para documentos digitalizados, instale também Tesseract e o idioma português. Ubuntu/Debian:

```sh
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

No Windows, instale Tesseract e adicione seu executável ao PATH. Se necessário, configure a variável de ambiente `TESSERACT_CMD` com o caminho do executável. O código não fixa uma instalação Windows para todos os usuários.

## Uso

```sh
python renomear_pdfs.py /caminho/para/copia --dry-run
python renomear_pdfs.py /caminho/para/copia
```

Faça backup e confira o preview antes de renomear. Nomes duplicados recebem sufixos; destinos existentes não são substituídos. A operação depende de suporte a hard links no sistema de arquivos e pode falhar em unidades que não os aceitam. Nesse caso, os erros são informados e o arquivo original é mantido.

Sem pytesseract/Tesseract, PDFs com texto ainda podem ser lidos, mas PDFs digitalizados precisam do OCR. A leitura pode falhar por formato diferente, scan ruim, permissões ou arquivo inválido. Confira os resultados: OCR não garante extração correta. Campos de processo e fornecedor precisam aparecer na mesma página, entre as duas primeiras.

Não inclua PDFs reais ou relatórios com dados internos no repositório. Use somente exemplos fictícios em demonstrações.
