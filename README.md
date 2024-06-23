# BuzzLibrary

<p align="center">
  <img src="assets/Group%206%20(1).png" alt="buzzlib">
</p>

A BuzzMonitor lançou sua nova iniciativa, a BuzzLibrary! Esta biblioteca online foi projetada para gerenciar estoque e realizar vendas de livros.

Com uma infraestrutura robusta, a BuzzLibrary é capaz de suportar um alto volume de requisições, garantindo estabilidade e eficiência mesmo diante de um grande número de clientes conectados simultaneamente. 

A plataforma está equipada para lidar com problemas de condições de corrida, assegurando que as operações de usuários ocorram de maneira fluida e sem intercorrências.

## Execução

Configure o venv e execute a aplicação com os comandos abaixo:

```bash
make setup
make run
```

> OBS: O arquivo .env contem a URI do BD utilizado para desenvolvimento, está no Github para fins de avaliação mas esse tipo de informação NÃO deve ser colocada em repositórios online. 

Este BD já está configurado com as migrações. Caso deseje usar outro BD, as migrations podem ser executadas com o seguinte comando:

```bash
make init-db
```

## Documentação das rotas

Rota base: `http://0.0.0.0:8080`


### Criação de livro

```bash
POST /book
```

**Corpo da Requisição (JSON):**

| Campo             | Tipo   | Obrigatório | Descrição                         |
|-------------------|--------|-------------|-----------------------------------|
| `author`          | String | Sim         | Nome do autor do livro.           |
| `title`           | String | Sim         | Título do livro.                  |
| `publication_year`| Inteiro| Sim         | Ano de publicação do livro.       |
| `stock`           | Inteiro| Sim         | Quantidade de estoque disponível. |
| `category`        | String | Sim         | Categoria do livro (ex: novel, education, etc.).|

**Exemplo de corpo da requisição:**

```json
{
  "author": "Agatha Christie",
  "title": "Assassinato no Expresso do Oriente",
  "publication_year": 1934,
  "stock": 1000,
  "category": "novel"
}
```

**Resposta Esperada:**

```bash
201 Created

{
  "author": "Agatha Christie",
  "title": "Assassinato no Expresso do Oriente",
  "publication_year": 1934,
  "stock": 1000,
  "category": "novel"
}
```

```bash
400 Bad Request

{
    "Missing fields": "title"
}
```

### Recuperar livros

```bash
GET /books?title=<title>&category=<category>
```

| Query             | Descrição | 
|-------------------|--------|
| `title`           | Filtrar por título |
| `category`        | Filtrar por categoria |

**Resposta Esperada:**

```json
200 OK
[
	{
        "author": "Agatha Christie",
        "title": "Assassinato no Expresso do Oriente",
        "publication_year": 1934,
        "stock": 1000,
        "category": "novel"
    }
]
```

### Recuperar um livro

```bash
GET /books/<id>
```

**Resposta Esperada:**

```json
200 OK
{
	"author": "aa",
	"category": "novel",
	"id": 1,
	"publication_year": 2024,
	"stock": 23,
	"title": "tt"
}
```

```json
400 Bad Request
{
	"message": "not found"
}
```

### Atualizar um livro

```bash
PUT /books/<id>
```

**Corpo da Requisição (JSON):**

| Campo             | Tipo   | Obrigatório | Descrição                         |
|-------------------|--------|-------------|-----------------------------------|
| `author`          | String | Não         | Nome do autor do livro.           |
| `title`           | String | Não         | Título do livro.                  |
| `publication_year`| Inteiro| Não         | Ano de publicação do livro.       |
| `stock`           | Inteiro| Não         | Quantidade de estoque disponível. |
| `category`        | String | Não         | Categoria do livro (ex: novel, education, etc.).|

**Exemplo de corpo da requisição:**

```json
{
  "author": "Agatha Christie",
  "title": "Assassinato no Expresso do Oriente",
  "publication_year": 1934,
  "stock": 1000,
  "category": "novel"
}
```

**Resposta Esperada:**

```bash
200 OK

{
  "author": "Agatha Christie",
  "title": "Assassinato no Expresso do Oriente",
  "publication_year": 1934,
  "stock": 1000,
  "category": "novel"
}
```

```bash
400 Bad Request

{
    "message": "not found"
}
```

### Deletar um livro

```bash
DELETE /books/<id>
```

**Resposta Esperada:**

```json
200 OK
{
	"success": true
}
```

```json
400 Bad Request
{
	"message": "not found"
}
```

### Criação de Pedidos

```bash
POST /purchase
```

**Corpo da Requisição (JSON):**

| Campo             | Tipo   | Obrigatório | Descrição                         |
|-------------------|--------|-------------|-----------------------------------|
| `book_id`          | Inteiro | Sim         | Id do livro.           |
| `quantity`         | Inteiro | Sim         | Quantidade de livros que se deseja comprar.|

**Exemplo de corpo da requisição:**

```json
{
    "book_id": 2, 
    "quantity": 1
}
```

**Resposta Esperada:**

```bash
201 Created

{
	"book_id": 2,
	"id": 2,
	"quantity": 1,
	"status": "Finished"
}
```

```bash
400 Bad Request

{
    "message": "Book not found."
}
```

```bash
400 Bad Request

{
	"message": "Insufficient stock. Refused!"
}
```

### Recuperar pedidos

```bash
GET /purchases
```

**Resposta Esperada:**

```json
200 OK
[
	{
		"book_id": 2,
		"id": 1,
		"quantity": 1,
		"status": "Finished"
	},
	{
		"book_id": 3,
		"id": 2,
		"quantity": 1,
		"status": "Finished"
	}
]
```


### Recuperar pedidos relacionados a um livro

```bash
GET /purchases/book/<book_id>
```

**Resposta Esperada:**

```json
200 OK
[
	{
		"book_id": 3,
		"id": 2,
		"quantity": 1,
		"status": "Finished"
	}
]
```

## Testes

Foi utilizada a biblioteca `unittest` para criação dos testes. A comunicação com o BD foi devidamente mockada utilizando `mock` de `unittest`.

Para rodar os testes, execute:

```
python -m unittest discover -s tests
```

O projeto se encontra com 93% de cobertura, como segue o report abaixo:

| Name                              | Stmts | Miss | Cover |
|-----------------------------------|-------|------|-------|
| src/__init__.py                   |    16 |    1 |   94% |
| src/book_service.py               |    44 |    0 |  100% |
| src/db.py                         |    10 |    0 |  100% |
| src/model.py                      |    75 |   19 |   75% |
| src/purchase_service.py           |    20 |    2 |   90% |
| tests/test_book_service.py        |   113 |    1 |   99% |
| tests/test_purchase_service.py    |    66 |    0 |  100% |
|-----------------------------------|-------|------|-------|
| TOTAL                             |   344 |   23 |   93% |


## Decisões arquiteturais

**MVC**

Foi escolhida a arquitetura MVC para construção dessa API, onde os modelos são definidos no arquivo `models.py`, os controladores estão nos arquivos `book_service.py` e `purchase_service.py`, e a view está definida em `routes.py`. Por ser uma API pequena, com poucos modelos e poucas rotas essa é uma estrutura que atende a demanda. Caso a API cresça, eu sugiro modularizar ainda mais os modelos, rotas e controladores.

**Race Conditions**

Caso haja muitos clientes acessando a API simultaneamente, pode ocorrer race conditions na realização do Pedido, por isso, foi implementado uma transaction no BD com o uso de `FOR UPDATE`, garantindo que a operação de pedido e alteração do estoque do livro sejam feitas de forma atômica.

**Soft Delete**

Foi utilizado o banco de dados relacional, PostgreSQL. Por isso, há um relacionamento entre as tabelas Book e Purchase. Sendo assim, um livro só pode ser removido se todas os pedidos que fazem referência a ele forem removidos em cascata. Para evitar a perda de pedidos com a remoção de livros, foi implementado um mecanismo de `soft delete`, dessa forma os livros deletados não estão disponíveis para o usuário mas os pedidos relacionados se mantem disponíveis no banco.

**Logs**

Todas as camadas da API possuem logs indicando a operação sendo realizada e se foi bem sucedida ou não. A mensagem de log está configurada no formato `'%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s'`, dessa forma é possível rastrear a hora realizada e a função que criou o log em questão. Todos os logs são direcionados para o terminal da aplicação, além de ficarem registrados no arquivo de caminho `/log/logs.log`.