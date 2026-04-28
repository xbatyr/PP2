-- groups table
CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- add default groups
INSERT INTO groups(name)
VALUES
    ('Family'),
    ('Work'),
    ('Friend'),
    ('Other')
ON CONFLICT (name) DO NOTHING;

-- add new fields to contacts
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS email VARCHAR(100),
    ADD COLUMN IF NOT EXISTS birthday DATE,
    ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);

-- save contact create time
ALTER TABLE contacts
    ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- table for extra phones
CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile'))
);
