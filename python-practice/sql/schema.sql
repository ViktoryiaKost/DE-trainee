CREATE TABLE IF NOT EXISTS rooms (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    birthday    DATE NOT NULL,
    sex         CHAR(1) NOT NULL
                CHECK (sex IN ('M', 'F')),
    room        INTEGER NOT NULL
                REFERENCES rooms (id)

);
