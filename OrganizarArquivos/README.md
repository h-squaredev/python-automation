# Organizador de arquivos

Agrupa arquivos de uma pasta e de suas subpastas por extensão, por exemplo `pdf/` e `jpg/`. Não apaga as pastas de origem e não processa links simbólicos de arquivos. Arquivos já na pasta correta são preservados. Nomes repetidos recebem sufixos numéricos.

Requer Python 3.10+. Usa apenas a biblioteca padrão.

```sh
python organizador_de_arquivo_1.py /caminho/para/copia --dry-run
python organizador_de_arquivo_1.py /caminho/para/copia
```

No Windows, coloque caminhos com espaços entre aspas. Escolha a pasta na linha de comando, sem editar o código.

Comece com uma cópia contendo arquivos fictícios. O modo real move arquivos e altera sua organização; mantenha backup. Não use a pasta do projeto como entrada. Arquivos sem extensão ficam como estão. Não execute enquanto outros programas estiverem modificando a pasta.
