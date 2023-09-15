create table urls
(
    id         bigint generated always as identity
        primary key,
    name       varchar(255) not null
        unique,
    created_at date         not null
);

alter table urls
    owner to katana;

