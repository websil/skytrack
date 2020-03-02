FROM postgres:11

COPY docker/postgres/initdb.d/ /docker-entrypoint-initdb.d/

WORKDIR /src

COPY docker/postgres/postgresql.conf.tpl /etc/postgresql/postgresql.conf

CMD ["-c", "config_file=/etc/postgresql/postgresql.conf"]