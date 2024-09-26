CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT
);

CREATE TABLE user_profiles (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER, 
    favorite_food TEXT, 
    bio TEXT, 
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE friends (
    id SERIAL PRIMARY KEY,
    user1 INTEGER NOT NULL,
    user2 INTEGER NOT NULL,
    status TEXT CHECK (status IN ('pending', 'accepted', 'rejected', 'deleted')) NOT NULL,
    CONSTRAINT fk_user1 FOREIGN KEY (user1) REFERENCES users(id),
    CONSTRAINT fk_user2 FOREIGN KEY (user2) REFERENCES users(id),
    CONSTRAINT unique_users UNIQUE (user1, user2),
    CONSTRAINT no_self_friendship CHECK (user1 <> user2)
);