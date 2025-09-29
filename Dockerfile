FROM python:3.11

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY ./app /code/app

ENV PYTHONPATH=/code

CMD ["poetry", "run", "python", "app/main.py", "--port", "80"]