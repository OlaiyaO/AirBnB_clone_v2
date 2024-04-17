-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create or update the user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';

-- Grant SELECT privilege on performance_schema
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

FLUSH PRIVILEGES
