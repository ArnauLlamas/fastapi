FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

COPY ./app /code

RUN pipenv install --deploy --system

# Clean
RUN pip uninstall -y pipenv virtualenv virtualenv-clone
RUN rm -f Pipfile*

EXPOSE 80

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]