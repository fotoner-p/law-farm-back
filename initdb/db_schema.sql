create table user
(
    id         int auto_increment
        primary key,
    email      varchar(99)          not null,
    password   varchar(99)          not null,
    is_active  tinyint(1) default 1 not null,
    username   varchar(30)          not null,
    created_at datetime             not null
);

create table bookmark
(
    id           int auto_increment                 primary key,
    user_id      int                                not null,
    content_type char(15)                           not null,
    created_at   datetime default CURRENT_TIMESTAMP not null,
    content_key  varchar(99)                        not null,
    constraint bookmark_user_id_fk
        foreign key (user_id) references user (id)
);

create table view_log
(
    id           int auto_increment                 primary key,
    user_id      int                                not null,
    created_at   datetime default CURRENT_TIMESTAMP null,
    content_key  varchar(99)                        not null,
    content_type char(15)                           not null,
    constraint content_log_user_id_fk
        foreign key (user_id) references user (id)
);

