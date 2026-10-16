"""
Inspeciona uma tabela Delta Lake da camada Bronze: schema, contagem de
linhas, partições e histórico de versões (transaction log).

Uso:
    python -m src.bronze.delta_info ta_cidadao
"""

import os
import sys
from pathlib import Path

from deltalake import DeltaTable
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python -m src.bronze.delta_info <tabela>")
        sys.exit(1)

    table = sys.argv[1]
    lakehouse_dir = Path(os.environ.get("LAKEHOUSE_DIR", "data/lakehouse"))
    delta_path = lakehouse_dir / "bronze" / table

    dt = DeltaTable(str(delta_path))

    print(f"Tabela: {table}")
    print(f"Versão atual: {dt.version()}")
    print(f"Linhas: {dt.to_pyarrow_table().num_rows}")
    print(f"\nSchema:")
    for field in dt.schema().to_pyarrow():
        print(f"  {field.name}: {field.type}")

    print(f"\nHistórico de versões:")
    for entry in dt.history():
        ts = entry.get("timestamp")
        op = entry.get("operation")
        print(f"  v{entry.get('version')} — {op} — {ts}")


if __name__ == "__main__":
    main()
