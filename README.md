# Authentication service

Service with API for authentication users and management

## Environment variables

The following environment variables are available to control the operation of the application:

 [environments.md](https://github.com/DzmitryZhybryk/authentication_service/blob/main/environments.md?plain=1)

.env file example:

```
DATABASE_URL=postgresql+psycopg://dzmitry_zhybryk:3050132596@postgres/authentication_database
DATABASE_PORT=5432
POSTGRES_USER=dzmitry_zhybryk
POSTGRES_PASSWORD=3050132596
POSTGRES_DB=authentication_database
POSTGRES_HOST=postgres
POSTGRES_HOSTNAME=127.0.0.1
POSTGRES_ECHO=True

REDIS_HOST=redis://redis/
REDIS_USERNAME=dzmitry_zhybryk
REDIS_PASSWORD=3050132596
REDIS_HASH_KEY=somedificultkey
DIGESTMOD=sha256
REDIS_DATABASE=0
REDIS_IO_THREADS=4
REDIS_IO_THREADS_DO_READS=true

USER_ROLES="admin,base_user,moderator"

PASSWORD="admin"

SECRET_KEY=somedificultkey
SALT=salt
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30
REFRESH_TOKEN_EXPIRE=30

API_KEY=somedificultkey

WORK_EMAIL=mr.zhybryk@gmail.com
WORK_EMAIL_PASSWORD=gjovrgkjcxurtztj

RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS=-rabbit log_levels [{connection,error},{default,error}] disk_free_limit 2147483648
BROKER_CONNECTION_RETRY_ON_STARTUP=True
```

## Before start up

For start up application you should have:

- [docker](https://www.docker.com/products/docker-desktop/)

## Start up

### Development mode

From directory with docker-compose file run command:

```bash
docker compose -f .\docker-compose-dev.yml up -d
```

## Database migration

```bash
alembic revision --autogenerate -m {revision_name}
alembic upgrade head
```

## Tests

### Unit-tests

```
Unit-tests run automatically when you push into feature/* branch
```

For start unit_tests inside docker:
```bash
docker build -f .\{Path_to_Dockerfile_unittests} . -t {container_name}
docker run --env-file {Path_to_env_file} {container_name}
```

example from root dir:

```bash
docker build -f .\Dockerfile_unittests . -t auth_unittests
docker run --env-file .env auth_unittests
```

### Integration-tests

```
Integration-tests run automatically after pull-request to the develop branch
```

For start integration_tests inside docker compose use command:

```bash
docker compose -f .\docker-compose-testing.yml up --abort-on-container-exit --build
```

## Swagger documentation

Documentation available on `/api/v1/docs/`
