import sys
from pathlib import Path

import pandas as pd


ORIGEM_PATH = Path("./src/origem-dados/origem-dados.csv")
TIPOS_PATH = Path("./src/tipos.csv")
INSERT_FILE = Path("./src/origem-dados/insert-dados.sql")

def load_file(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(file_path)

def filter_colums(frame: pd.DataFrame, col: str, filter: str) -> pd.DataFrame:
    return frame.query(f'{col}==@filter')
    
def sort_by_date(frame: pd.DataFrame, col: str) -> pd.DataFrame:
    frame[col] = pd.to_datetime(frame[col])
    
    return frame.sort_values(by=col)

def make_dict(frame: pd.DataFrame, index: str, value_col: str) -> dict:
    return frame.set_index(index)[value_col].to_dict()

def create_col_from_dict(frame: pd.DataFrame, dict: dict, index: str, target_col: str) -> pd.DataFrame:
    frame[target_col] = frame[index].map(dict)
    
    return frame

def frame_to_sql(frame: pd.DataFrame, file_path: Path, table_name: str) -> None:
    lines = []
    columns = ", ".join(frame.columns)
    
    for _, row in frame.iterrows():
        values = ", ".join(
            "NULL" if pd.isna(v) else f"'{v}'" if isinstance(v, str) else str(v)
            for v in row
        )
        lines.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
    
    sql = "\n".join(lines)
    
    file_path.write_text(sql, encoding='utf-8')
    
    return
    

def main() -> None:
    frame = load_file(ORIGEM_PATH)
    frame = filter_colums(frame, 'status', 'CRITICO')
    frame = sort_by_date(frame, 'created_at')
    
    tipos_frame = load_file(TIPOS_PATH)
    tipos = make_dict(tipos_frame, 'id', 'nome')
    
    frame = create_col_from_dict(frame, tipos, 'tipo', 'nome_tipo')
    
    frame_to_sql(frame, INSERT_FILE, 'dados_finais')
    
    
if __name__ == "__main__":
    try:
        main()
        
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        
        sys.exit()