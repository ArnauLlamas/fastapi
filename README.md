<!-- omit in toc -->

# FastAPI

Personal project trying out [FastAPI](https://fastapi.tiangolo.com) Python framework.

<!-- omit in toc -->

## Table of Contents

- [General info](#general-info)
- [Requirements](#requirements)
  - [Development](#development)

## General info

WIP

## Requirements

- VS Code + Remote Containers extension
- Docker
- Docker Compose

### Development

_This instruction imply you are using VSCode along with the Remote Containers extension, if you do not use any of them you will have to create the container by yourself, with such as `docker-compose up --build --detach development && docker-compose exec development bash`._

Once you open the downloaded repository with VSCode a popup asking you to reopen the repository in a remote container, ignore it for now.

The very first thing you will have to do is to create the `.env` files

- `.env` Specifies the variables for the docker-compose.yml and are developer-related. You can leave them blank and default values will be created, but you still need to create this file
- `.src/.env` Specifies the application variables

You will find examples of these files in the same directories where they are expected to live.

After that you can reopen the repository inside the container, open the VSCode palete in execution mode (`Ctrl + Shift + p`) and look for `Remote-Containers: Open folder in container...` (or similar).

Once inside the container type `make dev` to start the development server inside the container. VSCode should send another popup to check the browser on localhost:8000. Navigate to http://localhost:8000/docs to see the swagger documentation and try the API.
