# A04 — testes do sistema escolar fictício

Código do estudante:
Arquivo e interpretador executados:

## Retomada sem consulta
O que deve acontecer ao último registro quando a última entrada é inválida?
Minha resposta inicial: o ultimo registro continua intacto
O que get devolve? Como vírgula decimal é normalizada na A03?
Minha resposta inicial:get devolve oq foi digitado no entry, para ponto antes da conversao
Digitar um novo nome confirma uma nova consulta? Por quê?
Minha resposta inicial:nao pq esta apenas sendo digitado, para consultar tem q preencher tudo e calcular media

## Antes de programar
Quais valores pertencem ao mesmo registro confirmado?nome, turma, notas, media
Quantidade de notas exigida e intervalo permitido:5 notas de 0 a 10
Minha previsão para a média de 6, 7, 8, 9 e 10:8
Por que validar a quantidade antes de dividir? pq temq haver 5 as 5 notas para fazer o calculo de media

## Preveja e depois execute
Use identificação e notas fictícias. Nos casos com sequência, refaça o válido indicado.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular média | ausencia de registro |  | |
| T02 | Lia / T1 / notas 6, 7, 8, 9, 10 | media 8 |  | |
| T03 | Cinco notas zero, com identificação preenchida | media 0 | tods as notas aceitas | |
| T04 | Cinco notas 10, com identificação preenchida | media 10 | todas as notas aceitas | |
| T05 | Notas 7,5 / 8 / 6,5 / 9 / 7; repetir usando ponto decimal | media 7,6 | | |
| T06 | Após registrar T02, editar para Rui / T2 / cinco notas 5; somente Exibir |mantem registro de lia |apenas ediat nao confirma nada | |
| T07 | Após T02, tentar Rui / T2 / 5, 5, 5, 5, abc | informa q abc nao e valido| | |
| T08 | Corrigir a última nota de T07 para 5 e Calcular média | media 5 | registro passa a ser confirmado | |
| T09 | Nome vazio ou só espaços; repetir com turma vazia ou só espaços | nao aceita nenhum campo vazio | | |
| T10 | Cada nota vazia, só espaços ou letras; uma alteração por vez | nao ceita notas vazias, nem letras| | |
| T11 | Cada nota -0,1 ou 10,1; uma alteração por vez | nao aceitas notas fora do intervalo | | |
| T12 | Nome/turma/notas com espaços nas pontas; nome composto e acentos | aceita tudo  | | |
| T13 | Após um válido, Limpar campos e depois Exibir | limpa os campos | | |
| T14 | Notas 6 / 6 / 6 / 6 / 6,4; comparar média guardada e exibida | meddia 6,8 | | |
| T15 | No terminal, lista com quatro notas e depois seis; uma tentativa por vez | Rejeita quatro e seis notas | | |
| T16 | Fechar, reabrir e Exibir | Começa sem registro | | |

## Uso da interface
Percorri nome, turma, cinco notas e botões com Tab/Shift+Tab:
Acionei um botão usando o teclado: 
Conferi rótulos e redimensionamento:
Mensagem que precisei melhorar:
Colega que testou (código combinado):

## Fechamento sem consulta
Qual a diferença entre sum(notas) e len(notas)? sum() soma os valores da lista. len() conta quantos elementos existem nela.
Por que uma lista nova de números ajuda a preservar a confirmação? Porque cada tentativa começa com uma lista independente, evitando misturar as notas novas com as notas do último registro confirmado.
Qual dado o painel deve mostrar se eu editar a quinta nota sem calcular? Deve continuar mostrando as cinco notas, identificação e média do último cálculo confirmado.
Formatar com uma casa muda a média guardada? Não. A formatação altera somente a maneira como o número aparece na tela, não o valor armazenado.
Minha dificuldade, ajuste e próxima tentativa:

Entregas: medias.py, sistema_escolar.py e este registro preenchido.

## Teoria e transferência
Consigo explicar o que sum e len calculam.
Minha explicação:
Consigo distinguir uma lista de widgets de uma lista de textos/números.
Minha explicação:
Consigo prever o registro após erro na quinta nota.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre lista, laço, sum/len, cinco notas e confirmação integral:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
