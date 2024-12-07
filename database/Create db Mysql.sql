DROP DATABASE IF EXISTS `db_tareas`;
CREATE DATABASE `db_tareas`;

USE `db_tareas`;
SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;


DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`(
	`user_id` int NOT NULL AUTO_INCREMENT,
    `name` varchar (100) NOT NULL,
    `email` varchar(100) NOT NULL,
    `password` varchar(20) NOT NULL,
    `rol_id` int NOT NULL,
    PRIMARY KEY (`User_Id`)
);

DROP TABLE IF EXISTS `tasks`;

CREATE TABLE `tasks`(
	`task_id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `task_name` varchar (100) NOT NULL,
    `description` varchar(255),
    `date_due` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `status` boolean NOT NULL,
    PRIMARY KEY (`task_Id`),
    FOREIGN KEY (`user_id`) REFERENCES users(`user_id`)
);

DROP TABLE IF EXISTS `roles`;

CREATE TABLE `roles`(
	`rol_id` int NOT NULL AUTO_INCREMENT,
    `rol_name` varchar (100) NOT NULL,
    PRIMARY KEY (`rol_Id`)
);

ALTER TABLE users ADD CONSTRAINT rol_id FOREIGN KEY (rol_id) REFERENCES roles(rol_id);
ALTER TABLE tasks ALTER COLUMN status SET DEFAULT FALSE;