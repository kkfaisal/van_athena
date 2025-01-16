-- Create vector database user and database. Add your password
CREATE USER vector_user WITH PASSWORD '*****';
CREATE DATABASE vector_db;
GRANT ALL PRIVILEGES ON DATABASE vector_db TO vector_user;

-- Connect to vector database
\c vector_db;

-- Create the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Grant permissions to vector_user
GRANT ALL ON SCHEMA public TO vector_user;


-- Grant permissions on the tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vector_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vector_user;
