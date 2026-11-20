
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory
import sqlite3
from backup_sqlite import criar_backup


def verificar():
    with TemporaryDirectory() as pasta:
        origem = Path(pasta) / "origem.db"
        destino = Path(pasta) / "copia.db"

        with closing(sqlite3.connect(origem)) as banco:
            banco.execute("CREATE TABLE alunos (id INTEGER PRIMARY KEY, nome TEXT)")
            banco.execute("INSERT INTO alunos VALUES (41, 'Lia fictícia')")
            banco.commit()

        criar_backup(origem, destino)

        with closing(sqlite3.connect(destino)) as copia:
            assert copia.execute("SELECT nome FROM alunos WHERE id = 41").fetchone() == ("Lia fictícia",)
            assert copia.execute("PRAGMA integrity_check").fetchone()[0] == "ok"

        try:
            criar_backup(origem, destino)
        except FileExistsError:
            pass
        else:
            raise AssertionError("Backup não pode sobrescrever arquivo")

        try:
            criar_backup(Path(pasta) / "ausente.db", Path(pasta) / "outro.db")
        except FileNotFoundError:
            pass
        else:
            raise AssertionError("Origem ausente não pode criar banco")

    return True


if __name__ == "__main__":
    assert verificar()
    print("OK: backup, integridade, destino existente e origem ausente")
