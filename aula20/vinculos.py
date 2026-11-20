def validar_vinculos(alunos, planos, matriculas):
    def conferir_ids(registros, tipo):
        ids = set()
        for registro in registros:
            codigo = registro.get("id")
            if type(codigo) is not int or codigo <= 0 or codigo in ids:
                raise ValueError(f"ID inválido ou repetido em {tipo}.")
            ids.add(codigo)
        return ids

    ids_alunos = conferir_ids(alunos, "alunos")
    ids_planos = conferir_ids(planos, "planos")
    conferir_ids(matriculas, "matrículas")
    for matricula in matriculas:
        aluno_id = matricula.get("aluno_id")
        plano_id = matricula.get("plano_id")
        if type(aluno_id) is not int or aluno_id not in ids_alunos:
            raise ValueError("Matrícula com aluno inexistente.")
        if type(plano_id) is not int or plano_id not in ids_planos:
            raise ValueError("Matrícula com plano inexistente.")
    return True


def pode_excluir_aluno(codigo, matriculas):
    if type(codigo) is not int or codigo <= 0:
        raise ValueError("ID do aluno inválido.")
    return not any(matricula.get("aluno_id") == codigo for matricula in matriculas)
