CREATE TABLE Players(
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  name      TEXT, 
  position  TEXT, 
  team      TEXT
);
CREATE TABLE groups (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  key       TEXT    NOT NULL UNIQUE,
  password  TEXT,
  drafted   BOOLEAN NOT NULL DEFAULT false
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE users (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT    NOT NULL UNIQUE,
  password TEXT    NOT NULL,
  email    TEXT    UNIQUE
);
CREATE TABLE user_group_membership (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  groupID INTEGER NOT NULL,
  userID  INTEGER NOT NULL,
  role    TEXT    NOT NULL DEFAULT 'user',
  FOREIGN KEY (groupID) REFERENCES groups(id),
  FOREIGN KEY (userID)  REFERENCES users(id),
  UNIQUE (groupID, userID)
);
CREATE UNIQUE INDEX idx_groups_key ON groups(key);
CREATE UNIQUE INDEX idx_users_email ON users(email);
