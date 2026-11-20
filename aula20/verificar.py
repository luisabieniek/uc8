
from contextlib import closing
from vinculos import validar_vinculos, pode_excluir_aluno
from relacoes_sqlite import demonstrar
from backup_sqlite import criar_backup
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3


def verificar():
    alunos = [{"id": 41, "nome": "Lia"}]
    planos = [{"id": 7, "nome": "Plano"}]
    matriculas = [{"id": 101, "aluno_id": 41, "plano_id": 7}]

    assert validar_vinculos(alunos, planos, matriculas)
    assert not pode_excluir_aluno(41, matriculas)
    assert pode_excluir_aluno(92, matriculas)

    for alunos_teste, planos_teste, matriculas_teste in (
        (alunos, planos, [{"id": 101, "aluno_id": 99, "plano_id": 7}]),
        (alunos, planos, [{"id": 101, "aluno_id": 41, "plano_id": 99}]),
        ([{"id": True}], planos, matriculas),
        ([{"id": -1}], planos, matriculas),
        (alunos + alunos, planos, matriculas),
    ):
        try:
            validar_vinculos(alunos_teste, planos_teste, matriculas_teste)
        except ValueError:
            pass
        else:
            raise AssertionError("Vínculo inválido deveria ser recusado")

    assert demonstrar()

    with TemporaryDirectory() as pasta:
        origem = Path(pasta) / "origem.db"
        destino = Path(pasta) / "copia.db"

        with closing(sqlite3.connect(origem)) as banco:
            banco.execute("CREATE TABLE teste (id INTEGER PRIMARY KEY)")
            banco.execute("INSERT INTO teste VALUES (1)")
            banco.commit()

        criar_backup(origem, destino)

        with closing(sqlite3.connect(destino)) as banco:
            assert banco.execute("SELECT id FROM teste").fetchone() == (1,)

    return True


if __name__ == "__main__":
    assert verificar()
    print("OK: vínculos, IDs inválidos e integridade SQLite")
