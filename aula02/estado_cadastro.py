
# """A02 — prática 1: campos em edição e registro confirmado."""

# def registrar(campos, registro):
#     nome = campos["nome"].strip()
#     sobrenome = campos["sobrenome"].strip()
#     idade_texto = campos["idade"].strip()

#     if not nome or not sobrenome:
#         return "tem q por os dois ne garai."

#     try:
#         idade = int(idade_texto)
#     except ValueError:
#         return "idade tem que ser um numero ai garai"

#     if idade <= 0:
#         return "impossivel ter 0 anos."

#     registro.update({
#     "nome": nome,
#     "sobrenome": sobrenome,
#     "idade": idade
#     })

#     return "Cadastro registrado com sucesso."

# def exibir(registro):
#     if not registro:
#         return "Nenhum registro confirmado."

#     return (
#         f"Registro confirmado: {registro['nome']} "
#         f"{registro['sobrenome']}, {registro['idade']} anos."
#     )

# def limpar(campos):
#     campos["nome"] = ""
#     campos["sobrenome"] = ""
#     campos["idade"] = ""


# if __name__ == "__main__":
#     campos = {"nome": "Lia", "sobrenome": "Costa", "idade": "18"}
#     registro = {}
#     print(registrar(campos, registro))
#     print(exibir(registro))
#     limpar(campos)
#     print("Campos após limpar:", campos)
#     print(exibir(registro))
#     # Acrescente os outros cenários da matriz, um de cada vez.
