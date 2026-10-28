# Automações em Python

Três utilitários para tarefas com arquivos e documentos. Os projetos foram desenvolvidos com apoio de IA e estão em evolução para portfólio.

| Ferramenta | O que faz | Interface |
| --- | --- | --- |
| [Contador de páginas](ContadorPáginas/) | Soma páginas de PDFs em uma pasta e subpastas e exporta relatório | Tkinter |
| [Organizador de arquivos](OrganizarArquivos/) | Agrupa arquivos por extensão sem substituir arquivos existentes | Terminal, com `--dry-run` |
| [Renomeador de PDFs](RenomearPDFs/) | Extrai processo e fornecedor de PDFs com texto ou OCR e monta nomes | Terminal, com `--dry-run` |

## Preparação

Use Python 3.10 ou superior. Crie um ambiente virtual e instale as dependências:

```sh
python -m venv .venv
# Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

O contador requer Tkinter. No Ubuntu/Debian, instale `python3-tk` pelo gerenciador do sistema. O renomeador usa o programa Tesseract para PDFs digitalizados; veja as instruções na pasta dele.

## Segurança de uso

- Trabalhe com cópias e faça backup antes de mover ou renomear arquivos.
- Rode `--dry-run` antes da operação real. Ele não modifica arquivos.
- Não execute o organizador na pasta do código, em pastas do sistema ou em documentos originais sem backup.
- Não adicione documentos reais, credenciais, nomes de terceiros ou dados internos ao repositório. Os exemplos da versão atual devem ser fictícios.
- `.gitignore` é prevenção, não remove arquivos já versionados nem dados do histórico.

## Testes

```sh
python -m unittest discover -s tests -v
```

Os testes usam pastas temporárias e dados fictícios. Não comprovam compatibilidade em todos os sistemas nem medem economia de tempo. Teste a interface gráfica e o OCR na máquina em que serão usados.

## Estado do projeto

A documentação descreve o comportamento do código, sem prometer horas economizadas ou uso em produção.
