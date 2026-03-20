# Evertec test

## Pré-requisitos
 
- Python 3.11+
- pip
 
---
 
## Instalação
 
**1. Clone o repositório e acesse a pasta do projeto:**
 
```bash
git clone <url-do-repositorio>
cd <nome-do-projeto>
```
 
**2. Crie e ative o ambiente virtual:**
 
```bash
python -m venv .venv
```
 
```bash
# Linux/macOS
source .venv/bin/activate
 
# Windows
.venv\Scripts\activate
```
 
**3. Instale as dependências:**
 
```bash
pip install -r requirements.txt
```
 
---
 
## Execução
 
### 1. Extrair os dados
 
Extrai o arquivo `dados.zip` e move os CSVs para os diretórios corretos.
 
```bash
python src/extract.py
```
 
> Certifique-se de que o arquivo `src/dados.zip` existe antes de executar.
 
---
 
### 2. Gerar o SQL de inserção
 
Lê o `origem-dados.csv`, filtra os registros com status `CRITICO`, ordena por data e gera o arquivo `insert-dados.sql`.
 
```bash
python src/origem-dados/csv_to_sql.py
```
 
O arquivo gerado estará em:
 
```
src/origem-dados/insert-dados.sql
```
 
---
 
### 3. Iniciar a API
 
```bash
uvicorn src.main:app --reload
```
 
A API estará disponível em `http://localhost:8000`.
 
#### Endpoint disponível
 
| Método | Rota             | Descrição                     |
|--------|------------------|-------------------------------|
| GET    | `/tipos/{id}`    | Retorna o tipo pelo ID        |
 
**Exemplo de requisição:**
 
```bash
curl http://localhost:8000/tipos/1
```
 
**Exemplo de resposta:**
 
```json
{
  "id": 1,
  "tipo": "Nome do Tipo"
}
```
 
Documentação interativa disponível em `http://localhost:8000/docs`.
 
