#!/bin/bash

# This script initializes the database for the password manager application.

# Create the database if it doesn't exist
if [ ! -f "database.db" ]; then
    echo "Creating database..."
    touch database.db
fi

# Initialize tables
echo "Setting up tables..."
sqlite3 database.db <<EOF
CREATE TABLE IF NOT EXISTS vaults (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS passwords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vault_id INTEGER,
    password TEXT NOT NULL,
    FOREIGN KEY (vault_id) REFERENCES vaults (id) ON DELETE CASCADE
);
EOF

# Seed initial data (optional)
echo "Seeding initial data..."
sqlite3 database.db <<EOF
INSERT INTO vaults (name) VALUES ('Default Vault') ON CONFLICT(name) DO NOTHING;
EOF

echo "Database initialization complete."