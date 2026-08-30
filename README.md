# wsBackendFabricaDeSoftware26.2

Projeto Django (Workshop de Backend — Fábrica de Software 26.2).

## Descrição

API para cadastro de governadores e seus gastos públicos por mandato.
Cada gasto é registrado com categoria, valor, data, órgão responsável e
a URL da fonte oficial (Portal da Transparência, TCE, etc). A API também
consulta a API pública do IBGE para trazer informações complementares
dos estados já cadastrados.

Entidades relacionadas: um `Governador` pode ter vários `Gasto` (relação
1-N via chave estrangeira).

## Como instalar

```bash
git clone https://github.com/GuilhermePDD/wsBackendFabricaDeSoftware26.2.git
cd wsBackendFabricaDeSoftware26.2
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python -m pip install -r requirements.txt
python manage.py migrate
```

## Como rodar

```bash
python manage.py runserver
```

Servidor disponível em `http://127.0.0.1:8000/`.

Para acessar o painel administrativo (`/admin/`), crie um superusuário:

```bash
python manage.py createsuperuser
```

## Endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/api/governadores/` | Lista todos os governadores |
| POST | `/api/governadores/` | Cria um governador |
| GET | `/api/governadores/{id}/` | Detalha um governador |
| PUT/PATCH | `/api/governadores/{id}/` | Atualiza um governador |
| DELETE | `/api/governadores/{id}/` | Remove um governador |
| GET | `/api/gastos/` | Lista todos os gastos |
| POST | `/api/gastos/` | Cria um gasto (requer `governador` por ID) |
| GET | `/api/gastos/{id}/` | Detalha um gasto |
| PUT/PATCH | `/api/gastos/{id}/` | Atualiza um gasto |
| DELETE | `/api/gastos/{id}/` | Remove um gasto |
| GET | `/api/estados/` | Consulta a API do IBGE para os estados já cadastrados em `Governador` |
| GET | `/admin/` | Painel administrativo do Django |
