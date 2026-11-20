# Sorveteria — A18

## Executar

Requer Python 3 com Tkinter e SQLite (bibliotecas padrão). Abra o terminal nesta pasta.

```powershell
python verificar.py
python main.py
```

Na primeira execução, `produtos.db` é criado nesta pasta. Use uma cópia da pasta para testar sem alterar os dados originais. O catálogo inicial é `catalogo.json`. O relatório `vendas.csv` é gerado após a confirmação.

## Conferir

Cadastre um cliente, escolha um produto, adicione quantidade, selecione PIX e confirme. Para duas unidades de R$ 6,50, o total esperado é R$ 11,31. Teste também cancelar a prévia e tentar confirmar um produto com preço alterado.

## Limites

Interface Tkinter exige ambiente gráfico. O CSV é um relatório local; uma falha de gravação do CSV após a transação SQLite deve ser tratada como pendência de sincronização do relatório, sem duplicar a venda. Use apenas dados fictícios.
