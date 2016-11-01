drop table if exists users;
drop table if exists reviews;
create table users (
    id integer primary key autoincrement,
    wins integer DEFAULT 0,
    losses integer DEFAULT 0,
    email varchar(255),
    Google_OAuth_Token varchar(512)
);
