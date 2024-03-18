FROM python:3.12

WORKDIR /usr/bet_maker

ENV PATH="/root/.local/bin:${PATH}"
ENV POETRY_VERSION=1.8.2

COPY pyproject.toml ./
COPY poetry.lock ./

# Installation of Poetry and application dependencies
RUN : \
    && curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}\
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && :

COPY src .

COPY .env .
COPY logging_config.yaml .

COPY scripts .
COPY tests .

COPY alembic.ini .
COPY migrations .

ENV PYTHONPATH="${PYTHONPATH}:/usr/bet_maker/src"

CMD ["bash", "./scripts/start_app.sh"]
