# Authentication service

Service with API for authentication users and management

## Environment variables

The following environment variables are available to control the operation of the application:

- `JWT_ALGORITHM` - алгоритм шифрования;

.env file example:

```
JWT_ALGORITHM=HS256
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

## Swagger documentation

Documentation available on `/api/v1/docs/`