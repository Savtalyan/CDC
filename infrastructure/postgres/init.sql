
-- create a dedicated replication user 
CREATE USER debezium_user WITH REPLICATION LOGIN PASSWORD 'debezium_pass';

-- grant read access to tables that need to be captured
GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO debezium_user;

-- create the publication 
CREATE PUBLICATION debezium_publication FOR ALL TABLES;