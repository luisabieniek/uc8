from aluno import Aluno


def verificar_independencia():
    lia = Aluno()
    rui = Aluno()
    # TODO: comparar os objetos, suas listas, médias e alterações independentes.
    # TODO: usar assert nos resultados esperados; só então retornar True.
    assert lia is not rui
    assert lia.notas is not rui.notas

    assert lia.atualizar("Lia", "T1", ["8", "9", "7", "10", "6"]) == "Aluno atualizado com sucesso."
    assert rui.atualizar("Rui", "T2", ["5", "6", "7", "8", "9"]) == "Aluno atualizado com sucesso."

    assert lia.calcular_media() == 8.0
    assert rui.calcular_media() == 7.0

    lia.atualizar("Lia", "T1", ["10", "10", "10", "10", "10"])

    assert lia.calcular_media() == 10.0
    assert rui.calcular_media() == 7.0
    assert rui.nome == "Rui"
    assert rui.turma == "T2"
    assert rui.notas == [5, 6, 7, 8, 9]
   
    return True


def verificar_validacao():
    # TODO: válido seguido de erro; conferir preservação de todos os atributos.
    aluno = Aluno()

    assert aluno.atualizar("Ana", "T1", ["10", "9", "8", "7", "6"]) == "Aluno atualizado com sucesso."

    nome_anterior = aluno.nome
    turma_anterior = aluno.turma
    notas_anteriores = aluno.notas.copy()
    media_anterior = aluno.calcular_media()

    resultado = aluno.atualizar("Erro", "T2", ["1", "2", "3", "4", "11"])

    assert resultado != "Aluno atualizado com sucesso."

    assert aluno.nome == nome_anterior
    assert aluno.turma == turma_anterior
    assert aluno.notas == notas_anteriores
    assert aluno.calcular_media() == media_anterior

    # TODO: testar limites 0/10, vírgula e lista de textos independente.
    # TODO: retornar True somente depois das verificações implementadas.
    assert aluno.atualizar("Teste", "T3", ["0", "0", "0", "0", "0"]) == "Aluno atualizado com sucesso."
    assert aluno.calcular_media() == 0.0

    assert aluno.atualizar("Teste", "T4", ["10", "10", "10", "10", "10"]) == "Aluno atualizado com sucesso."
    assert aluno.calcular_media() == 10.0

    assert aluno.atualizar("Teste", "T5", ["6,5", "7,5", "8", "9", "10"]) == "Aluno atualizado com sucesso."
    assert aluno.calcular_media() == 8.2

    notas_texto = ["6", "7", "8", "9", "10"]
    assert aluno.atualizar("Teste", "T6", notas_texto) == "Aluno atualizado com sucesso."

    notas_texto[0] = "0"

    assert aluno.notas == [6, 7, 8, 9, 10]

    return True


if __name__ == "__main__":
    independencia = verificar_independencia()
    validacao = verificar_validacao()
    if independencia and validacao:
        print("Verificações do modelo concluídas.")
    else:
        print("Verificações incompletas; implemente e execute os casos.")
