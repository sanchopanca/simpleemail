CREATE TABLE channels (
	id INTEGER NOT NULL,
	name VARCHAR,
	PRIMARY KEY (id)
);

CREATE TABLE users (
	id INTEGER NOT NULL,
	login VARCHAR,
	password_hash VARCHAR,
	email VARCHAR,
	channel_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(channel_id) REFERENCES channels (id)
);

CREATE TABLE user_channel (
	user_id INTEGER,
	channel_id INTEGER,
	FOREIGN KEY(user_id) REFERENCES users (id),
	FOREIGN KEY(channel_id) REFERENCES channels (id)
);

INSERT INTO channels (name) VALUES ("User's Super Channel");
INSERT INTO users (login, password_hash, email, channel_id) VALUES
("user", "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8", "user@mail.org", 1);

INSERT INTO channels (name) VALUES ("User's Second Amazing Channel #2");
INSERT INTO users (login, password_hash, email, channel_id) VALUES
("user2", "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8", "user@mail.com", 2);