FROM python:3.8-bullseye

WORKDIR /usr/src/app

EXPOSE 8000

RUN apt-get update
RUN apt-get install -y mariadb-server
EXPOSE 3306
LABEL version="1.0"
LABEL description="MariaDB Server"

HEALTHCHECK --start-period=5m \
    CMD mariadb -e 'SELECT @@datadir;' || exit 1

COPY docker/entrypoint.sh ./
RUN chmod 755 entrypoint.sh

# Add poetry install location to PATH
ENV POETRY_VERSION=1.3.0
ENV POETRY_HOME=/opt/poetry
ENV PATH=/opt/poetry/bin:$PATH

# Install and configure Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.in-project true;

# Fake folders for install
RUN mkdir -p src/adminplatform
RUN touch src/adminplatform/__init__.py
RUN mkdir -p scripts
RUN touch scripts/__init__.py

# Install project 
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true --local
RUN poetry install --no-dev

# Copy scripts
ADD scripts ./scripts

# Copy project source code
ADD src ./src

# Copy migrations
COPY alembic.ini ./
ADD alembic ./alembic

# Execute migration and backend
ENTRYPOINT ./entrypoint.sh