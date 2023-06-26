All available environments:

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