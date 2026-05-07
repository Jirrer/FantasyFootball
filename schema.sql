CREATE TABLE Players(name text, position text, team text);
CREATE TABLE groups (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  key       TEXT    NOT NULL UNIQUE,
  password  TEXT    NOT NULL,
  drafted   BOOLEAN NOT NULL DEFAULT false
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE users (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  key      TEXT    NOT NULL UNIQUE,
  username TEXT    NOT NULL,
  email    TEXT    NOT NULL UNIQUE
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
CREATE UNIQUE INDEX idx_users_key  ON users(key);
CREATE UNIQUE INDEX idx_users_email ON users(email);
