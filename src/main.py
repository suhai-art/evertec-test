from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
from pathlib import Path

app = FastAPI(title="Tipos API", version="1.0.0")

CSV_PATH = Path("src/tipos.csv")


class TipoResponse(BaseModel):
    id: int
    tipo: str


def load_tipos() -> dict[int, str]:
    tipos = {}
    with open(CSV_PATH, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tipos[int(row["id"])] = row["nome"]
    return tipos


def find_tipo_by_id(tipo_id: int, tipos: dict[int, str]) -> str:
    tipo = tipos.get(tipo_id)
    if tipo is None:
        raise HTTPException(status_code=404, detail=f"Tipo com id '{tipo_id}' não encontrado.")
    return tipo


@app.get("/tipos/{tipo_id}", response_model=TipoResponse)
def get_tipo(tipo_id: int):
    tipos = load_tipos()
    tipo = find_tipo_by_id(tipo_id, tipos)
    return TipoResponse(id=tipo_id, tipo=tipo)