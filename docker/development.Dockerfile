FROM python:3.10

WORKDIR /code

ARG PACKAGES="\
    curl \
    wget \
    git \
    jq \
    make \
    lsb-release \
    "

ARG USERNAME
ARG USER_UID
ARG USER_GID

# Install basic packaging
RUN apt-get update && \
    apt-get install -y $PACKAGES

# Install Postgres 13 client
RUN wget -qO /etc/apt/trusted.gpg.d/pgdg.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -sc)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y postgresql-client-13

# Install pipenv
RUN pip install --upgrade pip && \
    pip install pipenv

# Install dependencies with pipenv
COPY Pipfile* app/
RUN cd app && \
    pipenv install --dev --system

# Add user
RUN groupadd --gid $USER_GID $USERNAME && \
    useradd --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    chown -R $USER_UID:$USER_GID /home/$USERNAME

USER ${USERNAME}

EXPOSE 8000

CMD ["/usr/bin/tail", "-f", "/dev/null"]