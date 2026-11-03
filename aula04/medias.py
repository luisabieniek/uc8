"""A04 — complete as funções e teste as cinco notas no terminal."""
def calcular(campos, registro):
     nome = campos["nome"].strip()
     turma = campos["turma"].strip()

     if not nome or not turma:
        return "Erro: nome e turma são obrigatórios."
    
     if len(campos["notas"]) != 5:
        return "Erro: informe exatamente cinco notas."
    
     notas = []
     
     for texto in campos["notas"]:
        try:
            nota = float(texto.strip())
        except ValueError:
            return "Erro: todas as notas devem ser numéricas."

        if nota < 0 or nota > 10:
            return "Erro: as notas devem estar entre 0 e 10."

        notas.append(nota)
        
        media = sum(notas) / len(notas)

        registro["nome"] = nome
        registro["turma"] = turma
        registro["notas"] = notas
        registro["media"] = media

        return "Cálculo realizado com sucesso."


def exibir(registro):
    if not registro:
        return "Nenhum cálculo foi realizado."

    return (
        f"Aluno: {registro['nome']}\n"
        f"Turma: {registro['turma']}\n"
        f"Notas: {registro['notas']}\n"
        f"Média: {registro['media']:.1f}"
    )



def limpar(campos):
    pass


if __name__ == "__main__":
    campos = {"nome": "Lia", "turma": "T1", "notas": ["6", "7", "8", "9", "10"]}
    registro = {}
    print(exibir(registro))
    print(calcular(campos, registro))
    print(exibir(registro))
    # Acrescente as sequências da matriz, prevendo antes de executar.
