CREATE TABLE IF NOT EXISTS urls(
    id         bigint generated always as identity primary key,
    name       varchar(255) not null unique,
    created_at date not null
);
CREATE TABLE IF NOT EXISTS url_checks(
    id          bigint generated always as identity primary key,
    url_id      bigint references urls,
    status_code integer,
    h1          varchar(255),
    title       varchar(255),
    description varchar(255),
    created_at  date
);