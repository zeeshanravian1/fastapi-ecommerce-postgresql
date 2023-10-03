# FastAPI Ecommerce Project with PostgreSQL

## Name

FastAPI Ecommerce Project

## Description

This project is built in [FastAPI](https://fastapi.tiangolo.com/) using python 3.11.
You can also use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations for this project.

## PostgreSQL Database

This project uses [PostgreSQL](https://www.postgresql.org/) database for storing data.

- You can download PostgreSQL by following commands:

```bash
# Create the file repository configuration:
sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql
```

- Run PostgreSQL shell by this command:

```bash
sudo -u postgres psql
```

- Change postgres password by this command:

```bash
ALTER USER <username> WITH PASSWORD '<password>';
```

- Create database by this command:

```bash
CREATE DATABASE IF NOT EXISTS <database_name>;
```

## Installation

- Configure [Pyenv](https://realpython.com/intro-to-pyenv/):
To configure pyenv you can follow this [tutorial](https://realpython.com/intro-to-pyenv/).

- Install mysql dependencies:
  
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

- Python Installation:
To run project, you must have python 3.11 installed on your system.
If python 3.11 is not installed pyenv will install it for you as you have already configured pyenv.

- Change Global Python Version:

```bash
pyenv global 3.11.0
```

- Configure [Poetry](https://python-poetry.org/):
Install poetry by following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Add poetry to path:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bash_rc
source ~/.bash_rc
```

Verify your poetry installation:

```bash
poetry --version
```

- Create Virtual Environment:
Go to project directory and type following command in terminal.

```bash
poetry shell
```

- Install Dependencies:
To install dependencies type following command in terminal.

```bash
poetry install
```

Verify your environment dependencies by running:

```bash
poetry show
```

## Configure [Alembic](https://alembic.sqlalchemy.org/en/latest/) for Database Migrations

- Type following command to initialize migrations

```bash
alembic init migrations
```

We have already added migrations folder to project, you can skip above step.

- Edit env.py in migrations folder to set path for your database:
We already have added path for database in env.py file and make required changes, you can skip this step as well.

- Your migrations

```bash
alembic revision --autogenerate -m "<Migration Name>"
```

- Apply Migrations

```bash
alembic upgrade heads
```

## Usage

- Pre Defined Roles:
Run roles_insertion.py from core/database_insertions to insert pre-defined roles

- Run FastAPI Server:
To run the FastAPI server run this command

```bash
uvicorn main:app --reload --host localhost --port 8000
```

- Access Swagger UI:
<http://0.0.0.0:8000/docs>

- Access Redoc UI:
<http://0.0.0.0:8000/redoc>
