import zipfile
import sys
from pathlib import Path

ZIP_PATH = Path("./src/dados.zip")
EXTRACT_DIR = Path("./src/.extract-tmp")

FILE_DESTINATION = {
    "origem-dados.csv": Path("./src/origem-dados"),
    "tipos.csv":        Path("./src"),
}

def extract_zip(zip_path: Path, destination: Path) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"ZIP not found: {zip_path}")

    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(destination)

def validate_files(directory: Path, filenames: list[str]) -> list[Path]:
    missing = [f for f in filenames if not (directory / f).exists()]

    if missing:
        raise FileNotFoundError(f"Missing files after extraction: {missing}")

    return [directory / f for f in filenames]


def move_files(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    source.replace(destination / source.name)
    
    
def load_data(zip_path: Path, extract_dir: Path, file_destination: dict[str, Path]) -> None:
    extract_zip(zip_path, extract_dir)
    paths = validate_files(extract_dir, list(file_destination.keys()))
    
    for path in paths:
        move_files(path, file_destination[path.name])

    return 

if __name__ == "__main__":
    try:
        data = load_data(ZIP_PATH, EXTRACT_DIR, FILE_DESTINATION)

    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)