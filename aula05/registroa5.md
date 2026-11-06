# A05 — organização e consultas do sistema escolar

Código do estudante:
Arquivos e interpretador executados:

## Retomada sem consulta
Quais dados devem ficar juntos no último registro válido?Nome, turma, as cinco notas e a média calculada.
Por que uma quinta nota inválida não pode alterar o nome confirmado?Porque todos os dados precisam ser validados antes de atualizar o registro. Se houver erro, o último registro válido deve permanecer intacto.
O que o botão recebe em command e quando essa função é executada?Recebe uma função sem parênteses, que será executada quando o usuário clicar no botão.
Minhas respostas iniciais:

## Antes de programar
Desenho dos pais: Tk → Frame base → grupos → campos e botões:
Onde cada grid organiza seus filhos?dentro do seu propio pai
Diferença entre edição, registro confirmado e retrato da consulta: edicao e os dados dgitados nos campos, registro confirmado sao os ultimos dados validos armazenados juntos, retrato da consulta e uma copia em texto dos dados confirmados quando a janela de consulta abre

## Preveja e depois execute
Dados sempre fictícios. C1/C2 identificam janelas de consulta diferentes.
| Caso | Sequência/verificação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Confirmar que nome/turma, cinco notas e ações possuem os grupos/pais planejados | Cada campo pertence ao grupo planejado. | | |
| T02 | Lia / T1 / 6,7,8,9,10; calcular e conferir média 8.0 | media deve ser 8 | media 8  | nao estava aparecendo a media quando consultava pq esqueci de por o return no final, rsrsrs |
| T03 | Antes do primeiro válido, usar Consultar | avisar que nao ha registro | nenhum registro | nenhum |
| T04 | Confirmar T02 e abrir consulta C1 | c1 mostra os dados de lia | mostrou os dados| nenhum |
| T05 | Editar Rui / T2 / cinco notas 5, sem calcular; observar C1 | c1 mantem os dados antigos | menteve os dados | nenhum |
| T06 | Após T02, tentar outra identificação com quinta nota abc; consultar novamente | ainda mostra registro de lia | ainda mostra registro de lia| nenhum |
| T07 | Corrigir e confirmar Rui / T2 / cinco notas 5; observar C1 e abrir C2 | c1 mostra lia e cc2 mostra rui| mostrava apenas o ultimo registro | modifiquei a funcao registro |
| T08 | Limpar as sete entradas; observar o registro principal e as consultas | campos limpam registros permanecem | campos limpam e consulta permanece | nenhum |
| T09 | Fechar C1 pelo botão; continuar usando a principal e C2 | fecha c1 e mantem c2| fecha c1 e mantem c2 | nenhum |
| T10 | Abrir outra consulta e fechá-la por Escape | esc fecha | esc fecha | nenhum |
| T11 | Abrir outra consulta e fechá-la pelo X da própria janela | x fecha consulta | x fecha consulta | nenhum |
| T12 | Repetir 0/10, fora de faixa, vazios, vírgula/ponto e identificação da A04 | validacoes continuam funcionando | validacoes continuem fincionando | nenhum |
| T13 | Percorrer grupos e botões por Tab/Shift+Tab; ampliar a janela e observar campos | teclado e redimencinamento funcionam| teclado e redimencionamneto funcionam | nenhum |
| T14 | Executar sem marca-a05.png; observar o cabeçalho textual | cabecalho textual aparece | cabecalho testual aparece| nada |
| T15 | Se usar PNG próprio, conferir imagem e testar arquivo inválido/ausente com fallback | imagem valida | imagem valida | nenhum |
| T16 | Executar o script a partir de outra pasta; conferir busca ao lado do script | funciona por causa do path __file__ | funciona | nenhum |
| T17 | Fechar a principal com consultas abertas; reabrir e tentar Consultar | fechar principal encerra tudo | encerrou tudo | nenhum |

## Imagem local (opcional)
O programa funcionou sem imagem:
Se criei PNG próprio, nome/origem do arquivo e teste realizado: 
Qual objeto conserva a referência da imagem:

## Fechamento sem consulta
Por que criar outra Tk/mainloop não é o contrato desta aula? pq o programa possui uma janela principal em loop, e as outras sao criadas em toplevel
Por que C1 pode manter o registro antigo depois de um novo válido? pq ela guarda o retrato dos dados existentes quando foi criada
Qual janela cada fechamento destrói?o botao fechar escape e x destroem somente a janela de consulta, fechar a janela primcipal encerra o programa e suas janelas
Minha dificuldade, correção e próxima tentativa: tive mais dificuldade em entender como se criava essa nova janela de consulta

Entregas: escolar_grupos.py, escolar_janelas.py e este registro.
Não há imagem obrigatória no pacote; use apenas arquivo próprio autorizado se optar por esse teste.

## Teoria e transferência
Consigo identificar o pai e a grade de um campo.
Minha explicação:cada widget pertence a um conteiner q e seu pai
Consigo explicar sticky e peso de coluna no redimensionamento.
Minha explicação:stick determina como o widget ocupa espaco e peso de coluna determina quanto espaco extra ela recebe quando a janela aumenta
Consigo distinguir edição, confirmado e retrato da consulta.
Minha explicação:edicao representa os dados digitados, confirmo representa os ultimos dados validos e retrato representa os dados copiados no momento de abertura
Ligação entre o ensaio e meus arquivos da atividade: ensaio ajudou a organizar os campos em grupos separar os dados editados dos confimados e criar janela de consulta
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados: scolar_grupos.py e escolar_janelas.py
Pasta e comando usados:  python escolar_janelas.py
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: 
Decisão do meu código sobre hierarquia de pais, expansão dos grupos, retratos e fechamento das Toplevel:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
