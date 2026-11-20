# UC8 — Desenvolvimento de Sistemas com Python

Este repositório reúne as atividades práticas desenvolvidas durante a **UC8**, organizadas da Aula 01 até a Aula 20.

O objetivo foi aprender e aplicar conceitos de programação em Python, começando com validações e funções simples e evoluindo para interfaces gráficas, orientação a objetos, persistência de dados e organização do código em módulos.

## Tecnologias utilizadas

- **Python 3** — linguagem principal do projeto.
- **Tkinter / ttk** — criação das interfaces gráficas.
- **JSON e CSV** — armazenamento e exportação de informações.
- **SQLite** — banco de dados local.
- **Git e GitHub** — versionamento dos arquivos.

As atividades usam principalmente bibliotecas que já acompanham o Python.

## Organização das aulas

| Aula | Conteúdo principal |
| --- | --- |
| 01 | Entrada de dados e validações iniciais. |
| 02 | Cadastro e controle do último registro válido. |
| 03 | Conversor de moedas com interface gráfica. |
| 04 | Sistema escolar com cálculo de médias. |
| 05 | Organização da interface em grupos e janelas de consulta. |
| 06 | Classe `Aluno`, orientação a objetos e testes do modelo. |
| 07 | Modelagem de produtos, itens e pedidos. |
| 08 | Evolução dos pedidos e cálculos de pagamento. |
| 09 | Regras e validações para a montagem de pedidos. |
| 10 | Produtos com variações e cálculos monetários. |
| 11 | Pizzaria: confirmação, cancelamento e estados do pedido. |
| 12 | Catálogo de produtos com leitura e gravação em JSON. |
| 13 | Perfis de acesso e relatórios de vendas em CSV. |
| 14 | Persistência de produtos com SQLite e repositório. |
| 15 | Cadastro de clientes e associação aos pedidos. |
| 16 | Separação de responsabilidades com controller e repositórios. |
| 17 | Continuidade da integração entre cadastro, vendas e banco de dados. |
| 18 | Revisão do sistema, execução de testes e documentação. |
| 19 | Criação de backup SQLite e verificação de integridade. |
| 20 | Validação de vínculos entre registros e restrições de chave estrangeira. |

Cada pasta contém os arquivos correspondentes àquela etapa. As aulas são versões e exercícios independentes: não é necessário executar todas em sequência para abrir uma atividade específica.

## Estrutura do repositório

```text
uc8/
├── aula01/
├── aula02/
├── aula03/
├── ...
├── aula18/
├── aula19/
│   ├── main.py
│   ├── verificar.py
│   ├── backup_sqlite.py
│   ├── produtos.db
│   └── ...
├── aula20/
│   ├── main.py
│   ├── verificar.py
│   ├── backup_sqlite.py
│   ├── relacoes_sqlite.py
│   ├── vinculos.py
│   └── ...
└── README.md
```

### Arquivos encontrados nas atividades

- `main.py`: inicia a interface da atividade, quando disponível.
- `modelos.py`: classes e regras relacionadas aos dados do sistema.
- `pagamento.py` / `pagamentos.py`: cálculos e validações de pagamento.
- `arquivos.py`: leitura e gravação do catálogo JSON.
- `banco.py`: operações com o banco SQLite.
- `repositorio.py` e `memoria.py`: acesso e armazenamento dos dados.
- `controller.py`: comunicação entre as ações do sistema e os repositórios.
- `perfis.py`: regras de acesso por perfil.
- `relatorios.py`: geração de relatórios CSV.
- `backup_sqlite.py`: criação de cópias de segurança do banco.
- `vinculos.py` e `relacoes_sqlite.py`: validação de referências e relações entre registros.
- `verificar.py` / `verificar_modelo.py`: testes automatizados de cada atividade.
- `registro*.md`: registros das atividades e testes realizados.

Nem todos esses arquivos estão presentes em todas as aulas, porque foram sendo adicionados conforme a evolução das atividades.

## Como executar

### 1. Preparar o ambiente

É necessário ter o **Python 3** instalado. Para conferir, abra o terminal do VS Code e execute:

```powershell
python --version
```

### 2. Abrir a aula desejada

No terminal, entre na pasta da atividade. Por exemplo:

```powershell
cd aula20
```

Se você estiver em outra pasta, primeiro navegue até a raiz do repositório.

### 3. Executar a aplicação

Nas aulas que possuem `main.py`:

```powershell
python main.py
```

Algumas atividades iniciais usam outro nome de arquivo, como `conversor.py`, `sistema_escolar.py` ou `escolar_janelas.py`.

### 4. Executar os testes

Quando existir `verificar.py`:

```powershell
python verificar.py
```

Nas atividades que possuem `verificar_modelo.py`:

```powershell
python verificar_modelo.py
```

Os testes devem ser executados **dentro da pasta da respectiva aula**, para que os imports e caminhos dos arquivos sejam encontrados corretamente.

## Funcionalidades trabalhadas

Ao longo das atividades, foram praticados:

- Validação de entradas e tratamento de erros com `try/except`.
- Funções, listas, dicionários e classes.
- Cálculo de médias, quantidades, subtotais e pagamentos.
- Interfaces com campos, botões, tabelas e janelas de consulta.
- Controle de estados, confirmação e cancelamento de operações.
- Leitura e gravação de dados em JSON.
- Geração de relatórios em CSV.
- Cadastro e consulta de informações em SQLite.
- Separação do código em modelos, controllers e repositórios.
- Backup de banco de dados e validação de integridade.
- Verificação de IDs, vínculos e chaves estrangeiras.
- Testes automatizados com `assert`.

## Cuidados ao testar

Os dados utilizados nas atividades são fictícios. Algumas operações alteram arquivos locais, como `produtos.db` e `vendas.csv`. Por isso, é recomendado fazer uma cópia da pasta antes de testar alterações no banco.

As interfaces Tkinter precisam ser executadas em um computador com ambiente gráfico. Os testes automatizados verificam regras específicas, mas não substituem a conferência manual da interface.

## Aprendizados

Este projeto mostra minha evolução durante a UC8, desde os primeiros exercícios de lógica até atividades com interfaces, banco de dados e módulos separados. Além de programar as funcionalidades, pratiquei organização de arquivos, identificação e correção de erros, testes e versionamento com Git.

---

**Projeto acadêmico — UC8 | Desenvolvimento de Sistemas com Python**
