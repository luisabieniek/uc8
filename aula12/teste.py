from pathlib import Path
from arquivos import carregar_catalogo

caminho = Path(__file__).with_name("catalogo.json")

ok, mensagem, catalogo = carregar_catalogo(caminho)

print(ok)
print(mensagem)

for produto in catalogo:
    print(produto.codigo, produto.nome, produto.preco_centavos)