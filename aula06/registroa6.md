# Meu registro A06 — objetos e módulos

Nome/código individual:
Turma e data:

## Hipóteses sem consulta
O que fica confirmado após erro na quinta nota? o ultimo registro valido permance confirmado 
Qual a diferença entre editar, confirmar e limpar? editar é modificar os campos que estao na janela, confimar valida todos os dados e atualizar o objeto aluno e limpar apaga os campos da tela sen apagar o ultimo registro confimado
O que aconteceria se dois nomes apontassem para o mesmo objeto? os dois nomes continuariam apontado para o mesmo objeto

## Arquitetura antes do código
Pasta com aluno.py, verificar_modelo.py e main.py:
Qual arquivo contém regras? aluno. Qual cria widgets? main. Quem importa quem? verificador e main importam aluno
O que __init__ cria em cada nova instância? inicializa os atributos proprios daql aluno como nome turma e notas
Por que duas chamadas Aluno() diferem de rui = lia? duas chamadas aluno() criam objetos independentes e rui = lia faz duas variaveis apontarem para o mesmo objeto 
O que self identifica em uma chamada de método? identifica a propia instancia que esta executando o metodo

## Testes executados
Preencha para cada caso: previsão | resultado observado | correção e nova tentativa.
Não marque como executado um teste ainda pendente.
- T01: Importar aluno sem Tk, sem janela e sem leitura de teclado.
  Previsão: Importar o modelo não deve abrir janela, importar Tkinter nem solicitar dados.
  Observado: nao abre janela
  Correção/reteste: nada
- T02: Criar dois objetos; listas distintas; ambos sem média antes de confirmar.
  Previsão: so e possivel confirmar se tiver media
  Observado: so e possivel confirmar se tiver media
  Correção/reteste: nao estava listando os registros, modifique o aluno para separar um em baixo do outro separado por registro
- T03: Lia/T1/[6,7,8,9,10] e Rui/T2/[5,5,5,5,5]; médias 8.0 e 5.0.
  Previsão: Lia deve ter média 8.0 e Rui média 5.0.
  Observado: lia tem media 8 e rui media 5
  Correção/reteste: nada
- T04: Atualizar só Lia; Rui mantém identificação, notas e média.
  Previsão: Alterar Lia não deve modificar nenhum dado de Rui.
  Observado:  nao modificou 
  Correção/reteste: nada
- T05: Após válido, tentar nome/turma vazios; preservar todo o registro.
  Previsão: 	nao aceita
  Observado: nao aceita 
  Correção/reteste: nada
- T06: Após válido, erro na quinta nota; preservar os três atributos e resumo.
  Previsão: nao valida se houver erro
  Observado: nao valida
  Correção/reteste: nada
- T07: Testar 0 e 10, vírgula/ponto, negativos, >10, nan, inf, vazio e texto.
  Previsão: nao aceita nada q nao seja de 0 a 10
  Observado: nao aceita nada doq nao seja de 0 a 10 
  Correção/reteste: nada
- T08: Recusar quantidade diferente de cinco notas, sem alterar o válido.
  Previsão: nao tem nem como por mais doq 5 notas
  Observado: n aceita mais doq 5 notas
  Correção/reteste: nada
- T09: Alterar a lista de textos original após atualizar; notas confirmadas não mudam.
  Previsão: Alterar a lista original não deve modificar as notas confirmadas.
  Observado: nao altera oq ja foi registrado
  Correção/reteste: nada
- T10: Executar verificar_modelo.py sem abrir GUI; cada assert corresponde a um caso.
  Previsão: Os testes devem executar sem abrir a interface e os assert devem verificar os resultados esperados.
  Observado: testes verificados 
  Correção/reteste: nada
- T11: Consultar antes do primeiro válido: orientação e nenhuma janela vazia.
  Previsão: aparece que nao ha nenhum registro
  Observado: aparece que nao ha nenhum registro
  Correção/reteste: nada
- T12: Confirmar Lia e abrir C1; editar Rui e errar a última nota: C1 e confirmado permanecem.
  Previsão: continua mostrando lia e o ultimo registro de rui.
  Observado: continua mostrando lia e ultimo registro
  Correção/reteste: nada
- T13: Corrigir e confirmar Rui; C2 mostra Rui e C1 conserva Lia.
  Previsão: c1 mostra rui e c2 mostra lia
  Observado: c1 mostra rui e c2 mostra lia
  Correção/reteste: nada
- T14: Limpar os sete campos; último registro e consultas continuam disponíveis.
  Previsão: limpar os campos nao alter aos registros
  Observado: limpar os campos nao altera os registros
  Correção/reteste: nada
- T15: Fechar consultas por botão, X e Escape; principal e outra consulta continuam funcionando.
  Previsão: fechar janela nao apaga ultimos registros
  Observado: fechar a janela nao apaga os registros
  Correção/reteste: nada
- T16: Conferir grupos, rótulos, expansão e percurso Tab; funcionar sem PNG.
  Previsão: funciona sem o png
  Observado: funciona sem png
  Correção/reteste: nada
- T17: Encerrar a principal e reabrir: começar sem registro; nenhum arquivo de dados gravado.
  Previsão: enecerrando a janela principal apaga todos os registros 
  Observado: encerar a janela principal apaga os registros
  Correção/reteste: nada 

## Explicação individual
Mostre dois objetos independentes e uma tentativa inválida após um válido.
Indique a linha que confirma o conjunto e por que a interface não repete a regra.
O que um assert verifica? Qual caso ainda falta?
Minha dificuldade e próximo teste:

Entrega: aluno.py, verificar_modelo.py, main.py e este registro.
Somente dados fictícios. A página não executa Python nem envia arquivos automaticamente.

## Teoria e transferência
Consigo apontar classe, instância, __init__ e self no exemplo.
Minha explicação:
Consigo provar que dois objetos mantêm dados independentes.
Minha explicação:
Consigo explicar a direção dos imports entre modelo, verificador e interface.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre classe, instância, listas próprias, confirmação integral e separação aluno/verificador/GUI:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
