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
- `POSTGRES_ECHO` - Flag for database logs;

- `USER_ROLES` - Basic user roles that will be created during application startup;

- `USERNAME` - Init user username, default=admin;
- `PASSWORD` - Init user password;
- `NICKNAME` - Init user nickname, default=admin;
- `EMAIL` - Init user email, default=admin@gmail.com;
- `ROLE` - Init user role, default=admin;

- `SECRET_KEY` - Secret key for generate JWT access tokens;
- `JWT_ALGORITHM` - Encryption algorithm;
- `ACCESS_TOKEN_EXPIRE` - Time to live JWT access token;

- `LOGGING_DIR` - Logs dir. Default = BASEDIR;
- `API_KEY` - Key for external API;
- `LOGURU_LEVEL` - Logging level;

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

USER_ROLES="admin,base_user,moderator"

PASSWORD="admin"

SECRET_KEY=somedificultkey
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=30

API_KEY=somedificultkey
LOGURU_LEVEL=INFO
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
