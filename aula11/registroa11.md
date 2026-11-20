# Meu registro A11 — Pizzaria: estados, confirmação e cancelamento

Nome/código individual, turma e data:

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Vazio não finaliza.
Previsão: pedido vazio sera recusado
Observado: pedido vazio e recusado
Correção/reteste ou pendência: nada

T02 — Forma ausente não finaliza.
Previsão: deve manter pedido aberto
Observado: foi recusado e manteve os itens
Correção/reteste ou pendência: nada

T03 — Cancelar, X e Escape preservam montagem e itens.
Previsão: deve fechar a previa e manter os itens
Observado:as tres acoes usam a mesma funcao
Correção/reteste ou pendência: nada

T04 — Prévia alterada depois da abertura exige nova conferência.
Previsão:deve pedir uma nova previa
Observado: confirmacao com a previa antiga foi recusada
Correção/reteste ou pendência: nda

T05 — Confirmar gera retrato com subtotal, desconto e total coerentes.
Previsão: 47 menos 6,11 de desconto da 40 ,89 no pix
Observado: ok
Correção/reteste ou pendência: nada

T06 — Pedido finalizado bloqueia mutações e segunda finalização.
Previsão:deve bloquear mudancas e nova confrmacao
Observado: todas as tentativas bloqueadas
Correção/reteste ou pendência: nada

T07 — Alterar o recibo retornado não altera o comprovante guardado.
Previsão:editar o recibo preserva a copia guardada
Observado: o codigo ainda nao guarda uma segunda copia
Correção/reteste ou pendência: nada

T08 — Novo pedido limpa a montagem; cancelamento de descarte preserva-a.
Previsão: confirmar limpa os campos 
Observado:limpar os itens comeca um novo peido
Correção/reteste ou pendência: nada

T09 — Principal continua utilizável após fechar confirmação.
Previsão: deve continuar funcionando
Observado: ok
Correção/reteste ou pendência: nada

## Explicação individual
Uma decisão que consigo justificar:
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados:
Caminho de dados fictícios usado (se houver):
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar estado e versão com papéis diferentes.
Minha explicação:
Consigo distinguir confirmação explícita de cancelamento.
Minha explicação:
Consigo justificar por que o comprovante precisa de um retrato independente.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre estados montagem/finalizado, versão da prévia e comprovante independente:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
