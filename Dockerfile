FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

# Встановлюємо залежності без інсталяції самого проєкту
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY . /app/

EXPOSE 8000

CMD ["python", "quotes_site/manage.py", "runserver", "0.0.0.0:8000"]
