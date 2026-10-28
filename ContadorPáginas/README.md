# Contador de páginas de PDF

Aplicação desktop Python/Tkinter para somar páginas de PDFs em uma pasta e subpastas, com registro dos arquivos que falharam e exportação de relatório de texto. Não altera os PDFs.

## Instalação

Requer Python 3.10+, Tkinter e pypdf:

```sh
python -m pip install pypdf
```

Tkinter costuma acompanhar a instalação do Python no Windows. No Ubuntu/Debian, instale `python3-tk` pelo gerenciador do sistema.

## Executar

```sh
python contador_pg.py
```

No Windows, `Executar.bat` também pode iniciar a ferramenta. Selecione a pasta, clique em iniciar e, após a contagem, salve o relatório se quiser.

A leitura roda em uma thread separada; mensagens chegam por uma fila e a interface é atualizada na thread principal. Arquivos com extensão `.pdf` ou `.PDF` são considerados. Links simbólicos de arquivos são ignorados.

## Limites

PDFs inválidos ou protegidos podem não ser contados e aparecem no registro de erros. O total inclui apenas arquivos lidos com sucesso. Não é uma validação contábil nem garante cobrança correta. Confira os resultados antes de usá-los em qualquer relatório de trabalho.

O relatório inclui nomes de arquivos, que podem ser sensíveis. Não publique relatórios de documentos reais. Use PDFs fictícios nas demonstrações. Não há garantia de aceitação por antivírus ou de compatibilidade em todo ambiente.
