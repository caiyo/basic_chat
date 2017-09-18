CREATE DATABASE challenge_kyle;

USE challenge_kyle;

CREATE TABLE user(
    user_guid varchar(36) NOT NULL PRIMARY KEY,
    username varchar(50) NOT NULL UNIQUE,
    displayname varchar(50),
    password varchar(100) NOT NULL,
    pass_salt varchar(100) NOT NULL,
    created_when datetime NOT NULL,
    updated_when datetime NOT NULL,
    deleted_when datetime NOT NULL DEFAULT '2050-01-01'
);

CREATE TABLE chat_group(
    group_id varchar(36) NOT NULL PRIMARY KEY,
    group_name varchar(50),
    is_public tinyint NOT NULL DEFAULT 0,
    created_by varchar(36),
    created_when datetime NOT NULL,
    updated_when datetime NOT NULL,
    deleted_when datetime NOT NULL DEFAULT '2050-01-01'
);

INSERT INTO chat_group(group_id, group_name, is_public, created_by, created_when, updated_when)
VALUES(uuid(), 'General', 1, 'root', now(), now());

CREATE TABLE chat_group_members(
    members_id varchar(36) NOT NULL PRIMARY KEY,
    group_id varchar(36) NOT NULL,
    user_id varchar(36) NOT NULL,
    last_viewed datetime,  
    created_when datetime NOT NULL,
    updated_when datetime NOT NULL,
    deleted_when datetime NOT NULL DEFAULT '2050-01-01'
);


CREATE TABLE chat_message(
    message_id varchar(36) NOT NULL PRIMARY KEY,
    group_id varchar(36) NOT NULL,
    created_by varchar(36) NOT NULL,
    message text,
    created_when datetime(3) NOT NULL,
    updated_when datetime NOT NULL,
    deleted_when datetime NOT NULL DEFAULT '2050-01-01'
);