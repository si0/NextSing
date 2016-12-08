-- 曲を格納するテーブル
create table ns_music (
    id serial primary key,
    music varchar(255) not null unique,
    artist integer not null,
    feeling integer not null,
    created timestamp not null default 'now'
);


-- アーティストを格納するテーブル
create table ns_artist (
    id serial primary key,
    artist varchar(255) not null unique,
    country integer not null,
    created timestamp not null default 'now'
);
insert into ns_artist (artist, country) values ('ONE OK ROCK', 1),
                                               ('LINKIN PARK', 2),
                                               ('BON JOVI', 2);


-- 静か、普通、激しいかを格納するテーブル
create table ns_feeling (
    id serial primary key,
    feeling varchar(15) not null,
    created timestamp not null default 'now'
);
insert into ns_feeling (feeling) values ('静か'), ('普通'), ('激しい');


-- 洋楽か邦楽かを格納するテーブル
create table ns_country (
    id serial primary key,
    country varchar(10) not null,
    created timestamp not null default 'now'
);
insert into ns_country (country) values ('邦楽'), ('洋楽');
