from contextlib import closing
import sqlite3


def demonstrar():
    with closing(sqlite3.connect(":memory:")) as banco:
        banco.execute("PRAGMA foreign_keys = ON")
        banco.execute("CREATE TABLE alunos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)")
        banco.execute("CREATE TABLE planos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)")
        banco.execute("""CREATE TABLE matriculas (
            id INTEGER PRIMARY KEY,
            aluno_id INTEGER NOT NULL REFERENCES alunos(id) ON DELETE RESTRICT,
            plano_id INTEGER NOT NULL REFERENCES planos(id) ON DELETE RESTRICT)""")
        banco.execute("INSERT INTO alunos VALUES (41, 'Lia fictícia')")
        banco.execute("INSERT INTO planos VALUES (7, 'Plano fictício')")
        banco.execute("INSERT INTO matriculas VALUES (101, 41, 7)")
        try:
            banco.execute("DELETE FROM alunos WHERE id = 41")
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("Exclusão vinculada deveria ser bloqueada")
        assert banco.execute("SELECT COUNT(*) FROM alunos").fetchone()[0] == 1
        assert banco.execute("SELECT COUNT(*) FROM matriculas").fetchone()[0] == 1
        return True


if __name__ == "__main__":
    assert demonstrar()
    print("OK: chave estrangeira bloqueou exclusão vinculada")
