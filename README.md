# rptgen
Gerador de relatórios -- RREO, RGF, DCASP etc

**Este é um pitch do sistema que será desenvolvido.**

# Objetivo
Gerar relatórios (RREO, RGF, DCASP etc) a partir dos dados do [pad-converter2](https://github.com/iddrs/pad-converter2) e outras fontes.


# Características

- Relatórios gerados no formato HTML e PDF (gerado a partir do HTML);
- Dados dos relatórios gerados em planilhas do MS Excel;
- Geração dos dados e dos relatórios em estapas separadas, possibilitando conferências e alterações pontuais dos dados;


# Síntese do processo

- Cada relatório é gerado a partir de um script de entrada. Por relatório entende-se cada um dos anexos do RREO, do RGF ou demonstração das DCASP.
- A geração do relatório se divide em duas etapas:
  - Carga e preparação dos dados: os daodos são carregados a partir das fontes de dados e preparados para serem salvos em uma pasta de trabalho do MS Excel. Para cada relatório é gerada uma pasta de trabalho. Para cada quadro do relatório é gerada uma planilha. Cada planilha é organizada da seguinte forma:
    - A primeira coluna da planilha tem os identificadores de linha;
    - As demais colunas representam cada uma das colunas do relatório, sendo que a primeira linha contém o identificador da coluna;
    - Cada célula, exceto as da primeira coluna (identificadores de linhas) e da primeira linha (identificadores de coluna) contém um valor a ser utilizado na criação do relatório.
  - Geração da saída em HTML e em PDF.


# Outros detalhes da implementação

- Desenvolvido em Python;
- Utiliza o mecanismo de template Jinja2 para a geração do HTML;
- A geração do template utiliza duas variáveis de dados:
  - `env`: carrega os dados gerais para o relatório, tais como período do relatório, assinantes, entidade, entre outras;
  - `dat`: recebe um objeto `DataRepo` que é um repositório dos dados a serem utilizados.
- Os dados após o processamento são armazenados em pastas separadas por período/grupo de relatório/relatório, como em:
  - `2023/12/DCASP/BalancoPatrimonial.xlsx`
  - `2023/4/RREO/Anexo2.xlsx`
  - `2023/6/RGF/Exec/Anexo1.xlsx`


# Sobre `DataRepo`

`DataRepo` é uma classe que vai prover os dados para o template.

No template, o acesso aos dados é feito da seguinte forma:

`dat.current.Frame.IdentificadoDeLinha.IdentificadorDeColuna()`

Por exemplo, para acessar o valor da coluna Previsão Atualizada da linha Receita Corrente do quadro de Receitas (do Balanço Orçamentário do RREO), o modelo deve utilizar:

`dat.current.Receitas.ReceitaCorrente.PrevisaoAtualizada()`

Caso existam dados de período anterior (como a coluna exercício anterior do balanço patrimonial, por exemplo), o acesso se dá por `dat.prev.Frame.IdentificadorDeLinha.IdentificadorDeColuna()`.
