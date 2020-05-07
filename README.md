# Flask Architecture

Arquitetura de exemplo para projetos utilizando Flask Framework

### Pré-requisitos

Python 3.6 ou superior
Pip 20.1 ou superior

### Instalação

Criação de um ambiente virtual:

```
python3 -m venv venv
```

Entrar no ambiente virtual com:

```
source venv/bin/activate
```

Instalar dependências com:

```
pip install -r requirements.txt
```

Criar tabelas do banco com:

```
flask db init
flask db migrate
flask db upgrade
```

### Rodar o projeto

```
flask run
```