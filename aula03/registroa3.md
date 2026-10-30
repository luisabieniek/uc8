# A03 — testes do conversor fictício

Código do estudante:
Arquivo e interpretador executados:

## Retomada sem consulta
O que Exibir deve ler quando os campos foram editados sem confirmação?
Minha resposta inicial:deve ler somente os registros da ultima conversao
Por que um erro não pode alterar parte do último registro válido?
Minha resposta inicial:
O que get devolve? Por que int não serve para uma idade escrita como 2.5?
Minha resposta inicial:metodo get() devolve um texto. int nao aceita decimais

## Antes de programar
Unidade das cotações: R$ por uma unidade de moeda (USD ou EUR). 
Operação escolhida para converter reais; justificativa por unidades: divisao, dividimos o valor em reais pela cotacao para representar quantos reais custam na moeda estrangeira
Quais entradas e resultados precisam pertencer à mesma tentativa? Reais, cotação do dólar, cotação do euro, resultado em dólares e resultado em euros.

## Preveja e depois execute
As cotações desta tabela são fictícias. Mantenha a ordem quando o caso indicar.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular | Deve informar que não existe conversão confirmada. | | nenhum |
| T02 | Calcular reais 100, cotação USD 5 e EUR 4 | USD 20,00 e EUR 25,00. | | nenhum |
| T03 | Editar para 200 / 10 / 8; somente Exibir | Deve continuar mostrando o cálculo anterior. | | nenhum |
| T04 | Após T02, Calcular com 200 / 10 / abc | Deve apresentar erro e preservar o registro anterior. | | nenhum |
| T05 | Corrigir para 200 / 10 / 8 e Calcular | Deve confirmar USD 20,00 e EUR 25,00. | | nenhum |
| T06 | Calcular com 100,50 / 5 / 4; repetir com 100.50 | Os dois formatos devem produzir os mesmos resultados. | | nenhum |
| T07 | Calcular com 0 / 5 / 4 | Deve aceitar e apresentar resultados iguais a zero. | | nenhum |
| T08 | Reais negativos; cada cotação 0 e negativa, um teste por campo | Deve recusar todas as entradas inválidas. | | nenhum |
| T09 | Cada campo vazio, só espaços ou abc, um por vez | Deve apresentar mensagem de erro e preservar o último cálculo. | | nenhum |
| T10 | Texto 1.000,50 ou 1,000.50; depois 1000,50 sem milhares | Os formatos com milhares devem ser recusados; 1000,50 deve ser aceito. | | nenhum |
| T11 | Após um válido, Limpar campos e depois Exibir | Deve limpar as entradas e preservar o último cálculo. | | nenhum |
| T12 | Calcular com 10 / 3 / 6; observar arredondamento de exibição | Deve apresentar USD 3,33 e EUR 1,67. | | nenhum |
| T13 | Fechar, reabrir e Exibir | Deve informar ausência de conversão, pois o registro fica somente em memória. | | nenhum |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab:
Usei o teclado para acionar um botão:
Mensagem que precisei melhorar:
Colega que testou (código combinado):

## Fechamento sem consulta
Por que a cotação precisa ser maior que zero, mas o valor em reais pode ser zero?
Como evitar mostrar uma entrada atual com um resultado anterior?
Formatar com duas casas muda o número guardado no registro?
Minha dificuldade, correção e próximo passo:

Entregas: calculos_moedas.py, conversor.py e este registro preenchido.

## Teoria e transferência
Consigo explicar por que a operação usa divisão.
Minha explicação:
Consigo distinguir normalização, conversão e formatação.
Minha explicação:
Consigo indicar quais dados devem ser confirmados juntos.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre unidades, conversão decimal, aproximação de float e confirmação conjunta das cinco chaves:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
