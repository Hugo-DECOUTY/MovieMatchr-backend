# MovieMatchr API
## Gitignore
To avoid having residual files from your favorite IDE, please create a global gitignore and add these lists:
- If you use VSCode: https://www.toptal.com/developers/gitignore/api/visualstudiocode
- If you use PyCharm: https://www.toptal.com/developers/gitignore/api/pycharm

### How to create global gitignore
1) Make the file as follows:
`vim ~/.gitignore_global`

2) Add the following file to Git's configuration:
`git config --global core.excludesfile ~/.gitignore_global`

## Requirements
### Windows
#### Chocolatey
```powershell
choco install -y python3 postgresql
```

#### Winget
```powershell
winget install -e --id Python.Python.3
winget install -e --id PostgreSQL.PostgreSQL
```

#### Without package manager
- [Python 3 (>= 3.10)](https://www.python.org/downloads/windows/)
- [PostgreSQL (>= 14.2)](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)

### Poetry
Follow installation instructions here: [Poetry Installation](https://python-poetry.org/docs/#installation)

## Configure
### Packages
#### Install
To prepare your environment:
```shell
poetry install
```

### PostgreSQL
TODO: Write documentation for configure PostgreSQL via `.env`

### Settings
To set settings, you need to copy `.env_template` and paste it in `.env`
```shell
cp .env_template .env
```

After that, configure as you like!
```shell
vim ./.env
```

> ℹ Info
>
> The file `.env` should not be pushed, because of sensitives datas.
> To avoid unpleasant surprises, we have added `.env` in `.gitignore`.

### Migrations
#### Running the Migration
On your first run or on update, make a migration for update your db:
```shell
poetry run alembic upgrade head
```

#### Creating a Migration Script
If you have change some things in `db_models`, make a migration file for update your db:
```shell
poetry run alembic revision
```

## Launch
To launch the backend, execute this command:
```shell
poetry run start
```

This application listens all requests passing through port 8000 of your server/computer.

## Develop
### Package
To install packages:
```shell
poetry add <PACKAGE_NAME>
```

## Production
### With docker
Set the settings, then launch the docker-compose:
```shell
docker-compose up --build -d
```

### Without docker
Follow installation guide, then execute:
```shell
poetry run prod
```
