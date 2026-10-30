"""A03 — complete as funções antes de conectá-las à janela."""
def calcular(campos, registro):
    try:
        reais = float(campos["reais"].replace(",", "."))
        cotacao_dolar = float(campos["cotacao_dolar"].replace(",", "."))
        cotacao_euro = float(campos["cotacao_euro"].replace(",", "."))
    except ValueError:
        return "Erro: entradas inválidas. Use apenas números."
    if reais < 0:
        return "Erro: valor em reais não pode ser negativo."
    
    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "Erro: cotações devem ser maiores que zero."
    
    dolares = reais / cotacao_dolar
    euros = reais / cotacao_euro

    registro.update({
        "reais": reais,
        "cotacao_dolar": cotacao_dolar,
        "cotacao_euro": cotacao_euro,
        "dolares": dolares,
        "euros": euros
    })
    return "Conversao relizada."


def exibir(registro):
    if not registro:
        return "Nenhuma convresao confirmada."
    return registro


def limpar(campos):
    pass


if __name__ == "__main__":
    campos = {"reais": "100", "cotacao_dolar": "5", "cotacao_euro": "4"}
    registro = {}
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))
    # Acrescente as outras sequências da matriz, prevendo antes de executar.
