# wsBackendFabricaDeSoftware26.2

Projeto Django (Workshop de Backend — Fábrica de Software 26.2).

## Descrição

API para cadastro de governadores e seus gastos públicos por mandato.
Cada gasto é registrado com categoria, valor, data, órgão responsável e
a URL da fonte oficial (Portal da Transparência do estado da Paraíba).
A API também consulta a API pública do IBGE para trazer informações
complementares (nome completo e região) dos estados já cadastrados.

Entidades relacionadas: um `Governador` pode ter vários `Gasto` (relação
1-N via chave estrangeira, `on_delete=PROTECT`).

O banco já vem populado (via migration de dados) com 4 governadores reais
da Paraíba e 2 gastos reais extraídos da API oficial de dados abertos do
estado (`api.dados.pb.gov.br`).

## Como instalar

```bash
git clone https://github.com/GuilhermePDD/wsBackendFabricaDeSoftware26.2.git
cd wsBackendFabricaDeSoftware26.2
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

## Como rodar

```bash
python manage.py runserver
```

- Painel visual: `http://127.0.0.1:8000/`
- Painel administrativo: `http://127.0.0.1:8000/admin/`
- Documentação interativa (Swagger): `http://127.0.0.1:8000/api/docs/`

## Autenticação

Todos os endpoints em `/api/` (exceto `/api/token/` e o painel em `/`)
exigem autenticação via **Token do Django REST Framework**.

1. Crie um usuário (`createsuperuser` ou pelo `/admin/`).
2. Obtenha o token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d "username=SEU_USUARIO&password=SUA_SENHA"
```

3. Use o token retornado no header das próximas requisições:

```
Authorization: Token <token retornado>
```

Pela interface do Swagger (`/api/docs/`), use o botão **Authorize** e cole
`Token <token>` para testar os endpoints direto do navegador.

## Endpoints

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| GET | `/` | Painel visual (ranking de gastos, dados do IBGE, tabela de gastos) | Não |
| GET | `/admin/` | Painel administrativo do Django | Login de sessão |
| POST | `/api/token/` | Obtém o token de autenticação | Não |
| GET/POST | `/api/governadores/` | Lista ou cria governadores | Token |
| GET/PUT/PATCH/DELETE | `/api/governadores/{id}/` | Detalha, atualiza ou remove um governador | Token |
| GET/POST | `/api/gastos/` | Lista ou cria gastos (requer `governador` por ID) | Token |
| GET/PUT/PATCH/DELETE | `/api/gastos/{id}/` | Detalha, atualiza ou remove um gasto | Token |
| GET | `/api/estados/` | Consulta a API do IBGE para os estados já cadastrados em `Governador` | Token |
| GET | `/api/schema/` | Schema OpenAPI (JSON) | Token |
| GET | `/api/docs/` | Interface Swagger interativa | Token |

## Diferenciais implementados

- Commits semânticos
- Organização de diretórios e boas práticas (app separada por
  responsabilidade: models, serializers, views, urls)
- Documentação (este README) e repositório no GitHub
- Página funcional com HTML/CSS (`/`)
- Tokens de autenticação (DRF Token Authentication)
- Swagger para documentação da API (`drf-spectacular`)
