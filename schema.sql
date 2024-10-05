CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
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

CREATE TABLE lunch_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    campus TEXT,
    restaurant TEXT,
    lunch_time TIMESTAMP NOT NULL,
    lunch_message TEXT,
    visibility TEXT CHECK (visibility IN ('public', 'friends')) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
);

CREATE TABLE lunch_responses (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_post FOREIGN KEY (post_id) REFERENCES lunch_posts(id),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);



