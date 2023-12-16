CREATE TABLE IF NOT EXISTS tracks (
    filename     TEXT        NOT NULL     UNIQUE,
    track        TEXT        NOT NULL,
    artist       TEXT,
    albumartist  TEXT,
    album        TEXT,
    genre        TEXT,
    year         INTEGER (4),
    tracknumber  INTEGER,
    discnumber   INTEGER,
    added_on     INTEGER,
    updated_on   INTEGER
);

CREATE TABLE IF NOT EXISTS config (
    id  TEXT PRIMARY KEY,
    val TEXT
);

INSERT INTO config(id,val)
VALUES('VERSION', '1.0')
ON CONFLICT DO NOTHING