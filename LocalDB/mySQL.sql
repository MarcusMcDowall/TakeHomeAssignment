-- PRAGMA foreign_keys = ON;

-- CREATE TABLE User (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL, userpsw TEXT NOT NULL);

-- CREATE TABLE Content (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, prompt TEXT NOT NULL, response TEXT NOT NULL, Created_timestamp TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES User (user_id));

-- PRAGMA foreign_keys;

-- INSERT INTO Content (id, user_id, prompt, response, Created_timestamp) 
-- VALUES (null, null, "What are you?", "I am an OPEN AI", "dd,ss,mm,yy");

-- DROP TABLE Content;
-- DROP TABLE User;