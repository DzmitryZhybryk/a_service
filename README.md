# Authentication service

Service with API for authentication users and management

## Environment variables

The following environment variables are available to control the operation of the application:

- `DATABASE_URL` - URL for database connect;
- `DATABASE_PORT` - Database port;
- `POSTGRES_USER` - Postgres user username;
- `POSTGRES_PASSWORD` - Postgres password;
- `POSTGRES_DB` - Postgres database name;
- `POSTGRES_HOST` - Postgres host;
- `POSTGRES_HOSTNAME` - Postgres host name;
- `POSTGRES_ECHO` - Flag for database logs, default=False;

- `REDIS_HOST`
- `REDIS_USERNAME`
- `REDIS_PASSWORD`
- `REDIS_HASH_KEY`
- `DIGESTMOD`
- `REDIS_HASH_KEY`
- `REDIS_DATABASE`
- `REDIS_IO_THREADS` - default=4
- `REDIS_IO_THREADS_DO_READS` - default=True

- `USER_ROLES` - Basic user roles that will be created during application startup;

- `USERNAME` - Init user username, default=admin;
- `PASSWORD` - Init user password;
- `NICKNAME` - Init user nickname, default=admin;
- `EMAIL` - Init user email, default=admin@gmail.com;
- `ROLE` - Init user role, default=admin;

- `SECRET_KEY` - Secret key for generate JWT access tokens and other secret information;
- `SALT` - Salt for generate secret information;
- `JWT_ALGORITHM` - Encryption algorithm;
- `ACCESS_TOKEN_EXPIRE` - Time to live JWT access token in minutes;
- `REFRESH_TOKEN_EXPIRE` - Time to live JWT refresh token in days;

- `LOGGING_DIR` - Logs dir, default=root dir;
- `API_KEY` - Key for external API;
- `LOGURU_LEVEL` - Logging level, default=INFO;

- `SMTP_SERVER_HOST` - host for send email, default=smtp.gmail.com;
- `WORK_EMAIL` - mail to send messages;
- `WORK_EMAIL_PASSWORD` - work email password;
- `SMTP_SERVER_PORT` - default=587

- `RABBITMQ_DEFAULT_USER` - default=admin
- `RABBITMQ_DEFAULT_PASS` - default=admin
- `RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS`
- `BROKER_CONNECTION_RETRY_ON_STARTUP`
- `RABBITMQ_BACKEND` - default=rpc://

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
docker compose -f .\docker-compose-test.yml up --abort-on-container-exit --build
```

## Swagger documentation

Documentation available on `/api/v1/docs/`
