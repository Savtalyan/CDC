-- Create role
CREATE ROLE app_role;

-- Create user
CREATE USER app_user
WITH PASSWORD 'super_secure_password';

-- Grant role to user
GRANT app_role TO app_user;

-- Create database
CREATE DATABASE app_db
    OWNER app_user;

-- Connect to the database
\c app_db

-- Grant database privileges
GRANT ALL PRIVILEGES ON DATABASE app_db TO app_user;

-- Allow role to use schema
GRANT USAGE, CREATE ON SCHEMA public TO app_role;

-- Create a sample table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Change ownership
ALTER TABLE users OWNER TO app_user;

-- Grant table privileges
GRANT SELECT, INSERT, UPDATE, DELETE
ON TABLE users
TO app_role;

-- Insert some mock data
INSERT INTO users (email, full_name)
VALUES
    ('alice@example.com', 'Alice Smith'),
    ('bob@example.com', 'Bob Johnson'),
    ('charlie@example.com', 'Charlie Brown');

-- Grant sequence privileges (needed for SERIAL)
GRANT USAGE, SELECT
ON SEQUENCE users_id_seq
TO app_role;