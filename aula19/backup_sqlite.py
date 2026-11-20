from contextlib import closing
from pathlib import Path
import sqlite3


def criar_backup(origem, destino):
    origem = Path(origem)
    destino = Path(destino)
    if not origem.is_file():
        raise FileNotFoundError("Banco de origem não encontrado.")
    if destino.exists():
        raise FileExistsError("Já existe um arquivo no destino.")
    if origem.resolve() == destino.resolve():
        raise ValueError("Origem e destino precisam ser diferentes.")
    with closing(sqlite3.connect(f"file:{origem.resolve().as_posix()}?mode=ro", uri=True)) as banco:
        with closing(sqlite3.connect(destino)) as copia:
            try:
                banco.backup(copia)
                resultado = copia.execute("PRAGMA integrity_check").fetchone()[0]
                if resultado != "ok":
                    raise ValueError("Falha na integridade do backup.")
            except Exception:
                copia.close()
                destino.unlink(missing_ok=True)
                raise
    return destino
