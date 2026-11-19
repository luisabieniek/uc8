# Meu registro A08 — Sorveteria: pagamentos e arredondamento

Nome/código individual, turma e data:

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — R$100,00 → 87,00 dinheiro/PIX; 92,00 débito; 100,00 crédito1x.
Previsão: 
Observado:
Correção/reteste ou pendência:

T02 — R$0,50 no PIX → R$0,44 com HALF_UP.
Previsão: 0,50 × 0,87 = 0,435. Arredondando com ROUND_HALF_UP resulta em R$ 0,44.
Observado:
Correção/reteste ou pendência: nada

T03 — Duas chamadas iguais produzem resultados iguais e não alteram os itens.
Previsão: produzem o mesmo resultado nenhum pedidio alterado
Observado: produzem o mesmo resultado com nenhum pedido alterado
Correção/reteste ou pendência: nada

T04 — Trocar PIX/crédito/PIX recalcula do subtotal original.
Previsão:  o ultimo resultado pix deve ser igal o primeiro
Observado: foi igual 
Correção/reteste ou pendência: nada

T05 — Forma vazia ou desconhecida: erro orientado.
Previsão: o sistema deve exibir mensagem de erro e pedido inalterado
Observado: apresnetou a mensagem e nao alterou o pedido
Correção/reteste ou pendência: nada

T06 — Valor com letras, NaN/inf, negativo, milhares ou mais de duas casas: recusar.
Previsão: entradas invalidas sao recusadas e mostra uma mensagem de erro 
Observado: mostou a mensagem e nao alterou nada
Correção/reteste ou pendência: nada

T07 — Subtotal = desconto +total após arredondamento.
Previsão:  a soma do desconto com o total final deve corresponder ao subtotal 
Observado: correspondeu ao subtotal
Correção/reteste ou pendência: nada

T08 — Validações de quantidade e catálogo da A07 preservadas.
Previsão: ok
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
Consigo distinguir subtotal, desconto e total.
Minha explicação:
Consigo explicar por que Decimal recebe texto e onde ocorre o arredondamento.
Minha explicação:
Consigo prever o efeito de repetir uma conferência sem mudar os itens.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre funções puras de pagamento, Decimal de texto, ROUND_HALF_UP e subtotal preservado:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
