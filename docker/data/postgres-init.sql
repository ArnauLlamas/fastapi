-- connect to test_td database
\c test_db

-- STRUCT
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE role AS ENUM ('admin', 'user', 'guest');

CREATE TABLE users (
  id uuid DEFAULT uuid_generate_v4 (),
  "name" varchar NOT NULL,
  password varchar NOT NULL,
  email varchar NOT NULL,
  "role" role NOT NULL,
  PRIMARY KEY (id),
  UNIQUE ("name"),
  UNIQUE (email)
);

-- DATA
-- password = secret
INSERT INTO users (id, name, password, email, role)
VALUES ('765bdd21-71bc-4869-9b31-bd37ef84284c', 'pepe', '$2b$12$ls.cL.bbv0VXgPH36DJX9uLU.Q2j2R9dWtQcJ/SCXmJNhGQ3s.zpW', 'pepe@example.com', 'admin');
