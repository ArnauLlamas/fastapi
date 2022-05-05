FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install and configure poetry
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false

COPY ./app /code

RUN poetry install --no-dev

# Clean
RUN pip uninstall -y poetry
RUN rm -f pyproject.toml poetry.lock

EXPOSE 80

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]