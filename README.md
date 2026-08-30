# wsBackendFabricaDeSoftware26.2

Projeto Django (Workshop de Backend — Fábrica de Software 26.2).

## Descrição

API + página de visualização sobre gastos de governadores da Paraíba por
mandato. Cada `Governador` tem um ou mais `Gasto` associados (relação 1-N
via chave estrangeira). O valor de cada `Gasto` cadastrado hoje representa
o **total real apurado do mandato inteiro** — soma de todas as notas de
empenho, de todos os órgãos do estado, mês a mês, do início ao fim do
mandato — calculado a partir da API oficial de dados abertos da Paraíba
(`api.dados.pb.gov.br`). A API também consulta a API pública do IBGE para
trazer nome completo e região dos estados já cadastrados.

## Status dos requisitos

**Obrigatórios (100% concluído):**
- CRUD completo com 2+ entidades relacionadas por FK (`Governador` → `Gasto`)
- Consumo de API externa com tratamento de erro (`try/except`, status codes)
- `.gitignore`, `requirements.txt`, `README.md`
- Nome do repositório correto (`wsBackendFabricaDeSoftware26.2`)

**Diferenciais implementados:**
- Commits semânticos
- Organização de diretórios e boas práticas
- Documentação (este README) e GitHub
- Página funcional com HTML/CSS (`/`)
- Tokens de autenticação (DRF Token Authentication)
- Swagger para documentação da API (`drf-spectacular`)

**Diferenciais não implementados (escolha do autor, por tempo/escopo):**
- Banco de dados externo (MySQL/PostgreSQL) — o projeto usa SQLite
- Docker-compose

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

Os endpoints de CRUD (`/api/governadores/`, `/api/gastos/`, `/api/estados/`)
exigem autenticação via **Token do Django REST Framework**. O painel visual
(`/`), a obtenção de token (`/api/token/`) e a documentação Swagger
(`/api/schema/`, `/api/docs/`) são públicos — não pedem token, pra permitir
explorar a API antes de autenticar.

Obtenha um token assim:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ -d "username=SEU_USUARIO&password=SUA_SENHA"
```

Use o token retornado no header das próximas requisições:

```
Authorization: Token <token retornado>
```

Pela Swagger UI (`/api/docs/`), use o botão **Authorize** e cole
`Token <token>`.

## Endpoints

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| GET | `/` | Painel visual (cofrinhos por governador + dados do IBGE) | Não |
| GET | `/admin/` | Painel administrativo do Django | Login de sessão |
| POST | `/api/token/` | Obtém o token de autenticação | Não |
| GET/POST | `/api/governadores/` | Lista ou cria governadores | Token |
| GET/PUT/PATCH/DELETE | `/api/governadores/{id}/` | Detalha, atualiza ou remove um governador | Token |
| GET/POST | `/api/gastos/` | Lista ou cria gastos (requer `governador` por ID) | Token |
| GET/PUT/PATCH/DELETE | `/api/gastos/{id}/` | Detalha, atualiza ou remove um gasto | Token |
| GET | `/api/estados/` | Consulta a API do IBGE para os estados já cadastrados em `Governador` | Token |
| GET | `/api/schema/` | Schema OpenAPI (JSON) | Não |
| GET | `/api/docs/` | Interface Swagger interativa | Não |

## Metodologia e decisões técnicas

### Por que "total apurado do mandato" e não uma amostra

A primeira versão do projeto cadastrava manualmente **1 gasto de exemplo**
por governador, extraído de uma única nota de empenho da API oficial.
Isso deixou claro um problema: pegar 1 registro dá um número na casa dos
milhões (o valor de 1 nota, de 1 órgão, em 1 mês), enquanto o total real
de um mandato inteiro está na casa das **dezenas de bilhões** — a diferença
não é erro da API, é a diferença entre um item individual e um agregado.

Para resolver isso de verdade (e não só cosmeticamente), foi escrito um
script (`somar_gastos_pb.py`, fora do controle de versão do projeto —
ferramenta de apuração, não parte da aplicação) que:
1. Para cada mês dentro do intervalo exato do mandato de cada governador,
   consulta `GET /despesas/orcamentarias?ano=X&mes=Y&page=N&per_page=1000`;
2. Soma o campo `valorEmpenhado` de **todos os registros de todas as
   páginas** daquele mês (a API pagina os resultados; um mês comum tem
   2 a 7 mil registros);
3. Soma os totais mensais para chegar ao total do mandato.

Esse total é o que está gravado como `Gasto.valor` hoje — por isso o
`categoria` desses registros é literalmente
`"Total apurado do mandato (todos os órgãos, elaboração própria via API
oficial)"`, deixando explícito que é um número **computado por nós a
partir de dados oficiais**, não um número publicado pronto pelo governo.
Isso importa para honestidade dos dados: `fonte_url` aponta pro dataset
oficial de onde os números vieram, mas a soma em si é nossa.

**Limite assumido conscientemente**: os meses de transição entre
mandatos (ex: quando um governador sai e outro assume no meio do ano) são
atribuídos por completo a quem ficou a maior parte do mês, já que a API
só filtra por mês inteiro, não por dia. Não valia a pena complicar o
script pra dividir um mês entre dois governadores por causa de poucos
dias de diferença.

### Por que Token do DRF e não JWT

Ambos cumprem o diferencial "tokens de autenticação". O Token do DRF foi
escolhido por ser **mais simples de configurar e explicar**: é uma string
opaca de 40 caracteres por usuário, sem expiração automática, guardada
numa tabela (`authtoken_token`) — o servidor consulta o banco a cada
requisição pra saber de quem é. JWT exigiria configurar geração/validação
de assinatura e política de expiração/refresh, complexidade que não
agregava valor ao escopo do desafio.

### Tratamento de erro também no DELETE (não só na API externa)

O enunciado pede tratamento de erro explicitamente para o consumo da API
externa, mas durante os testes foi encontrado outro ponto real: como
`Gasto.governador` usa `on_delete=PROTECT`, tentar apagar um `Governador`
que já tem gastos cadastrados fazia o Django levantar `ProtectedError` sem
tratamento, resultando num **erro 500 cru** (com `DEBUG=True`, isso expõe
a página de debug do Django pra quem chamar a API). Corrigido sobrescrevendo
`destroy()` em `GovernadorViewSet` pra capturar `ProtectedError` e devolver
`409 Conflict` com uma mensagem clara — sem isso, qualquer avaliador que
tentasse apagar um governador com gasto veria uma tela de erro feia em vez
de uma resposta de API decente.

### Por que a API do IBGE, e por que ela é separada do CRUD

O requisito pede consumo de "endpoint gratuito" com tratamento de erro —
não pede que a API externa alimente os dados principais do CRUD. Por
isso a consulta ao IBGE (`/api/estados/` e a seção "Dados dos estados" no
painel) é **só leitura**, isolada dos models `Governador`/`Gasto`: ela
nunca escreve no banco, então não corre risco de misturar dado real
cadastrado manualmente/apurado com dado de uma API que pode falhar ou
ficar fora do ar.

### Por que os números do painel trocam de formato ao passar o mouse

Os totais em bilhões (`R$ 77.115.197.185,87`) são difíceis de ler de
relance num cartão pequeno. A solução foi mostrar por padrão um formato
resumido (`R$ 77.12B`) e revelar o valor exato só ao passar o mouse sobre
o cofrinho — implementado **inteiramente em CSS** (seletor `:hover` +
irmão geral `~`), sem JavaScript, consistente com o resto da página que
não usa nenhum script.

### Por que um filtro de template customizado para formatação monetária

O filtro próprio (`gastos_politicos/templatetags/gastos_extras.py`,
`brl` e `brl_compacto`) foi criado quando o `LANGUAGE_CODE` do projeto
ainda estava em `en-us` — os filtros nativos do Django formatavam número
no padrão americano, e trocar a localização inteira do projeto na época
afetaria outras partes (datas, admin) sem necessidade.

Depois o `LANGUAGE_CODE` foi trocado para `pt-br` (e `TIME_ZONE` para
`America/Recife`), o que já deixa datas e textos do admin em português
automaticamente (ex: "30 de Agosto de 2026" na tabela de gastos). Mesmo
assim, o filtro `brl` continua sendo usado: ele não depende de nenhuma
configuração de localização pra funcionar (é formatação Python pura), o
que o torna mais previsível — funcionaria igual mesmo se o
`LANGUAGE_CODE` mudasse de novo no futuro.

### Problemas de ambiente encontrados (Windows)

- **`pip install` falhando com "Fatal error in launcher"**: a pasta do
  projeto fica em `Área de Trabalho` (tem acento). O launcher do
  `pip.exe` grava o caminho do Python como texto fixo no executável, e
  caracteres acentuados corrompem esse caminho. Contornado usando
  `python -m pip install ...` em vez de `pip install ...` (usa o
  `python.exe` direto, sem depender do launcher `pip.exe`).
- **Script de apuração sem mostrar progresso**: o Python bufferiza a
  saída padrão quando ela não vai pra um terminal interativo (como
  quando roda em background). Resolvido rodando com `python -u`
  (unbuffered).

## Limitações conhecidas (não corrigidas, escopo de projeto de disciplina)

- `SECRET_KEY` e `DEBUG=True` estão como o `django-admin startproject`
  gera por padrão, direto no `settings.py` versionado — aceitável para
  rodar localmente/avaliação, mas **não deve ir pra produção** assim. Em
  produção real, isso viraria variável de ambiente (`.env`, já ignorado
  pelo `.gitignore`) e `DEBUG=False`.
- A consulta ao IBGE no painel (`/`) é feita a cada carregamento da
  página, sem cache — se o IBGE estiver lento, a página demora junto
  (até o timeout de 5s por estado consultado). Não é um bug, é uma
  simplificação consciente: o projeto tem poucos estados cadastrados
  (hoje só PB), então o custo é baixo.
