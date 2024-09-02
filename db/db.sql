-- ---
-- Globals
-- ---

-- SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
-- SET FOREIGN_KEY_CHECKS=0;

-- ---
-- Table 'user'
-- 
-- ---

DROP DATABASE recomendation_app_db;

CREATE DATABASE IF NOT EXISTS recomendation_app_db;

USE recomendation_app_db;

DROP TABLE IF EXISTS `user`;
		
CREATE TABLE `user` (
  `user_id` INTEGER NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL UNIQUE,
  `password` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL UNIQUE,
  `name` VARCHAR(20) NOT NULL,
  `last_name` VARCHAR(20) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT (NOW()),
  PRIMARY KEY (`user_id`)
);

-- ---
-- Table 'place'
-- 
-- ---

DROP TABLE IF EXISTS `place`;
		
CREATE TABLE `place` (
  `place_id` VARCHAR(50) NOT NULL,
  `placename` VARCHAR(50) NOT NULL,
  `rating` FLOAT DEFAULT NULL,
  `phone` VARCHAR(50) DEFAULT 'NULL',
  `maps_url` VARCHAR(100) DEFAULT 'NU1LL',
  PRIMARY KEY (`place_id`)
);

-- ---
-- Table 'prompt'
-- 
-- ---

DROP TABLE IF EXISTS `prompt`;
		
CREATE TABLE `prompt` (
  `prompt_id` INTEGER NOT NULL AUTO_INCREMENT,
  `created_at` TIMESTAMP NOT NULL DEFAULT (NOW()),
  `user_id` INTEGER NOT NULL,
  PRIMARY KEY (`prompt_id`)
);

-- ---
-- Table 'answer'
-- 
-- ---

DROP TABLE IF EXISTS `answer`;
		
CREATE TABLE `answer` (
  `answer_id` INTEGER NOT NULL AUTO_INCREMENT,
  `created_at` TIMESTAMP NOT NULL DEFAULT (NOW()),
  `prompt_id` INTEGER NOT NULL,
  PRIMARY KEY (`answer_id`)
);

-- ---
-- Table 'user_place'
-- 
-- ---

DROP TABLE IF EXISTS `user_place`;
		
CREATE TABLE `user_place` (
  `user_id` INTEGER NOT NULL,
  `place_id` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`user_id`, `place_id`)
);

-- ---
-- Foreign Keys 
-- ---

ALTER TABLE `prompt` ADD FOREIGN KEY (user_id) REFERENCES `user` (`user_id`);
ALTER TABLE `answer` ADD FOREIGN KEY (prompt_id) REFERENCES `prompt` (`prompt_id`);
ALTER TABLE `user_place` ADD FOREIGN KEY (user_id) REFERENCES `user` (`user_id`);
ALTER TABLE `user_place` ADD FOREIGN KEY (place_id) REFERENCES `place` (`place_id`);

SELECT * FROM answer;
SELECT * FROM place;
SELECT * FROM user;
SELECT * FROM user_place;
SELECT * FROM prompt;

INSERT INTO `user` (`username`,`password`,`email`,`name`,`last_name`) VALUES
('avherrera','123456789','aleviherrera@gmail.com','Alejandro','Villa'),
('avhe','123456789','avh@gmail.com','Antonio','Herrera');

-- ---
-- Table Properties
-- ---

-- ALTER TABLE `user` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `place` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `prompt` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `answer` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
-- ALTER TABLE `user_place` ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- ---
-- Test Data
-- ---

-- INSERT INTO `user` (`user_id`,`username`,`password`,`name`,`last_name`,`created_at`) VALUES
-- ('','','','','','');
-- INSERT INTO `place` (`place_id`,`placename`,`rating`,`phone`,`maps_url`,`prompt_id_prompt`) VALUES
-- ('','','','','','');
-- INSERT INTO `prompt` (`prompt_id`,`created_at`,`user_id`) VALUES
-- ('','','');
-- INSERT INTO `answer` (`answer_id`,`created_at`,`prompt_id`) VALUES
-- ('','','');
-- INSERT INTO `user_place` (`user_id`,`place_id`) VALUES
-- ('','');