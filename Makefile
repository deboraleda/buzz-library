.PHONY: setup run init-db migrate-db

# Define o nome do ambiente virtual
VENV_NAME := venv

# Define o caminho para o executável do Python 3
PYTHON := python3

init-db:
	@echo "Inicializando o banco de dados..."
	@flask db init
	@flask db migrate -m "Initial migration for book table"
	@flask db upgrade
	@echo "Banco de dados inicializado e migrado com sucesso."

setup:
	@echo "Criando ambiente virtual..."
	@$(PYTHON) -m venv $(VENV_NAME)
	@echo "Ambiente virtual criado."

	@echo "Instalando dependências..."
	@$(VENV_NAME)/bin/pip install -r requirements.txt
	@echo "Dependências instaladas."

	@echo "Ambiente de desenvolvimento está pronto."

run:
	@echo "Executando a aplicação..."
	@source $(VENV_NAME)/bin/activate && PYTHONPATH=${PYTHONPATH}:$(PWD) && $(VENV_NAME)/bin/python app.py
