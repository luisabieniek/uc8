# A02 — estados e transições do cadastro

Código do estudante:
Arquivo e interpretador executados:

## Retomada sem consulta
1. O que get devolve? Por que int pode falhar? 
Minha resposta inicial: get obtem o texto digitado na entrada, int pode falhar quando texto nao for um numero valido
2. O que muda entre passar uma função e chamá-la ao ligar um botão?
Minha resposta inicial:
3. Que caso detecta um nome preenchido somente com espaços?
Minha resposta inicial: strip

## Preveja e depois execute (nomes sempre fictícios)
| Caso | Estado/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Registrar | informa q nao exite cadastro confirmado | | nenhum |
| T02 | Registrar Lia / Costa / 18 e Exibir | lia costa, 18 anos |  | nenhum |
| T03 | Editar para Rui / Lima / 22; somente Exibir | Continuará exibindo Lia Costa, 18 anos. | | nenhum |
| T04 | Limpar campos e depois Exibir | As entradas ficarão vazias e Lia continuará confirmada. | | nenhum |
| T05 | Após um válido, tentar registrar outro nome com idade abc | Aparecerá um erro e o cadastro anterior será preservado. | | nenhum |
| T06 | Registrar Rui / Lima / 22; depois Exibir | Rui Lima, 22 anos, substituirá Lia Costa. | | nenhum |
| T07 | Nome vazio ou somente espaços | O cadastro será recusado com mensagem de erro. | | nenhum |
| T08 | Sobrenome vazio ou somente espaços | O cadastro será recusado com mensagem de erro. | | nenhum |
| T09 | Idade vazia, 0, -2 e 2.5 (um teste por entrada) | Todas as tentativas serão recusadas. | | nenhum |
| T10 | Espaços nas pontas e nome composto | Os espaços das pontas serão removidos e o nome composto será aceito. | | nenhum |
| T11 | Fechar, reabrir e Exibir | O programa informará que não existe cadastro confirmado. | | nenhum |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab:
Mensagem que precisei melhorar:
Colega que testou (código fictício ou combinado):

## Fechamento sem consulta
Por que Limpar campos não deve apagar o registro confirmado?
pq esta so limpando oq esta sendo escrito e nao oq ja foi registrado
Como uma tentativa inválida pode estragar um cadastro anterior se a ordem do código estiver errada?

Minha dificuldade, ajuste e próximo passo:

Entregas externas: estado_cadastro.py e cadastro_completo.py, além deste registro.
