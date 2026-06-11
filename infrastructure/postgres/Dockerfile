FROM postgres:16

COPY init.sql /docker-entrypoint-initdb.d/
COPY scripts/schema.sql /docker-entrypoint-initdb.d/