START TRANSACTION;
SET time_zone = "+00:00";

CREATE DATABASE IF NOT EXISTS `epytodo` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `epytodo`;

CREATE TABLE IF NOT EXISTS `task` (
  `task_id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `begin` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end` timestamp NOT NULL DEFAULT DATE_ADD(CURRENT_TIMESTAMP(), INTERVAL 1 DAY),
  `status` enum('not started','in progress','done') NOT NULL DEFAULT 'not started',
  `private` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`task_id`)
);

CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE IF NOT EXISTS `user_has_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fk_user_id` int(11) NOT NULL,
  `fk_task_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`fk_user_id`),
  KEY `fk_task_id` (`fk_task_id`)
);


ALTER TABLE `user_has_task`
  ADD CONSTRAINT `fk_task_id` FOREIGN KEY (`fk_task_id`) REFERENCES `task` (`task_id`),
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`fk_user_id`) REFERENCES `user` (`user_id`);
COMMIT;