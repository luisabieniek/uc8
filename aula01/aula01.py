"""A01 — prática 1. Use somente nome e idade fictícios."""

def conferir(nome, idade_texto):
    # TODO: retirar espaços nas pontas e recusar nome sem texto.
    # TODO: converter idade para int, tratar ValueError e exigir idade > 0.
    # TODO: retornar mensagem coerente; não gravar arquivos.
    return "Complete a função conferir antes de concluir os testes."




def conferir(nome, idade_texto):
    nome = nome.strip()
    if not nome:
        return "nome tem que ser um texto ai garai"
    
    try:
        idade = int(idade_texto)
    except ValueError:
        return "idade tem que ser um numero ai garai"
    
    if idade <= 0:
        return "idade tem que ser maior que 0 ai garai"
    
    return f"Nome: {nome}, Idade: {idade}"


if __name__ == "__main__":
    nome = input("Nome fictício: ")
    idade_texto = input("Idade fictícia: ")
    print(conferir(nome, idade_texto))





    
