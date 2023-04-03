FROM python:3.11.2-slim-buster
ENV PYTHONBUFFERED=1
ENV PAGINATE_BY=5

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# FROM python:3.10-slim

# WORKDIR /app
#
# RUN pip install poetry
# COPY poetry.lock .
# COPY pyproject.toml .
# RUN poetry install --no-root
#
# COPY alembic alembic
# COPY alembic.ini .
#
# COPY src src