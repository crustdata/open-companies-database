
## Prerequisites

- [Pyenv](https://github.com/pyenv/pyenv)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Local Development

Follow these steps to set up the environment and run the server on your host machine with the database in a Docker container.

### 1. Clone the Repository

```shell
git clone https://github.com/crustdata/open-companies-database.git
cd open-companies-database
```

### 2. Install Python Dependencies

Make sure you have Poetry installed and is using python 3.12.3+ via `pyenv`

1. Install Python 3.12.3 via `pyenv`:

    ```
    pyenv install 3.12.3
    ```

2. Configure Poetry to use Python 3.12.3:

    ```
    pyenv shell 3.12.3
    poetry env use ~/.pyenv/versions/3.12.3/bin/python
    ```

3. Install the dependencies:

    ```
    poetry install
    ```

### 3. Set Up the Database Container

Start the PostgreSQL database container:
```shell
docker-compose up -d db
```

### 4. Set Environment Variables

Set the `DJANGO_SETTINGS_MODULE` to use the development settings:

```shell
export DJANGO_SETTINGS_MODULE=open_companies_database.settings_dev
```

### 5. Apply Migrations

Run the following command to apply database migrations:
```shell
poetry run python manage.py migrate
```

### 6. Run the Development Server

Start the Django development server:
```shell
poetry run python manage.py runserver
```
Your application should now be running at `http://127.0.0.1:8000`.
