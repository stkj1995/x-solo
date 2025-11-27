SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";
SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `x`;
USE `x`;


CREATE TABLE IF NOT EXISTS `users` (
`user_pk` char(32) NOT NULL,
`user_email` varchar(100) NOT NULL,
`user_password` varchar(255) NOT NULL,
`user_username` varchar(20) NOT NULL,
`user_first_name` varchar(20) NOT NULL,
`user_last_name` varchar(20) NOT NULL DEFAULT '',
`user_avatar_path` varchar(50) NOT NULL,
`user_verification_key` char(32) NOT NULL,
`user_verified_at` bigint(20) UNSIGNED NOT NULL,
PRIMARY KEY (`user_pk`),
UNIQUE KEY `user_email` (`user_email`),
UNIQUE KEY `user_username` (`user_username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `users` VALUES
('u001', '[sophie@example.com](mailto:sophie@example.com)', 'scrypt:hash1', 'sophie', 'Sophie', 'Teinvig', 'avatar_1.jpg', '', 1700000000),
('u002', '[daniel@example.com](mailto:daniel@example.com)', 'scrypt:hash2', 'daniel', 'Daniel', '', 'avatar_2.jpg', 'key123', 0),
('u003', '[mille@example.com](mailto:mille@example.com)', 'scrypt:hash3', 'mille', 'Mille', '', 'avatar_3.jpg', 'key456', 0),
('u004', '[anna@example.com](mailto:anna@example.com)', 'scrypt:hash4', 'anna', 'Anna', 'Larsen', 'avatar_4.jpg', '', 1700001000),
('u005', '[max@example.com](mailto:max@example.com)', 'scrypt:hash5', 'max', 'Max', '', 'avatar_5.jpg', '', 1700002000),
('u006', '[lara@example.com](mailto:lara@example.com)', 'scrypt:hash6', 'lara', 'Lara', '', 'avatar_6.jpg', 'key789', 0);



CREATE TABLE IF NOT EXISTS `posts` (
`post_pk` char(32) NOT NULL,
`post_user_fk` char(32) NOT NULL,
`post_message` varchar(280) NOT NULL,
`post_total_likes` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
`post_image_path` varchar(255) NOT NULL,
PRIMARY KEY (`post_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `posts` VALUES
('p001', 'u001', 'Hello world!', 0, 'post_1.jpg'),
('p002', 'u002', 'My first post', 0, ''),
('p003', 'u003', 'Testing posts', 0, 'post_2.jpg'),
('p004', 'u001', 'Another day, another post', 0, ''),
('p005', 'u004', 'Excited to join!', 0, 'post_3.jpg'),
('p006', 'u005', 'Good morning everyone', 0, ''),
('p007', 'u006', 'Loving this platform', 0, 'post_4.jpg');



CREATE TABLE IF NOT EXISTS `comments` (
`comment_pk` char(32) NOT NULL,
`comment_post_fk` char(32) NOT NULL,
`comment_user_fk` char(32) NOT NULL,
`comment_message` varchar(255) NOT NULL,
`comment_created_at` bigint(20) UNSIGNED NOT NULL,
PRIMARY KEY (`comment_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `comments` VALUES
('c001', 'p001', 'u002', 'Nice post!', 1700000100),
('c002', 'p001', 'u003', 'I agree!', 1700000200),
('c003', 'p002', 'u001', 'Welcome!', 1700000300),
('c004', 'p004', 'u004', 'Cool update!', 1700000400),
('c005', 'p005', 'u001', 'Congrats!', 1700000500),
('c006', 'p006', 'u003', 'Good morning!', 1700000600);


CREATE TABLE IF NOT EXISTS `follows` (
`follow_pk` char(32) NOT NULL,
`follow_user_fk` char(32) NOT NULL,
`follow_target_fk` char(32) NOT NULL,
PRIMARY KEY (`follow_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `follows` VALUES
('f001', 'u001', 'u002'),
('f002', 'u003', 'u001'),
('f003', 'u004', 'u001'),
('f004', 'u005', 'u003'),
('f005', 'u006', 'u002');



CREATE TABLE IF NOT EXISTS `likes` (
`like_pk` char(32) NOT NULL,
`like_post_fk` char(32) NOT NULL,
`like_user_fk` char(32) NOT NULL,
PRIMARY KEY (`like_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `likes` VALUES
('l001', 'p001', 'u002'),
('l002', 'p002', 'u001'),
('l003', 'p003', 'u004'),
('l004', 'p004', 'u003'),
('l005', 'p005', 'u001'),
('l006', 'p006', 'u005'),
('l007', 'p007', 'u006');



CREATE TABLE IF NOT EXISTS `languages` (
`language_pk` char(32) NOT NULL,
`language_code` varchar(10) NOT NULL,
`language_name` varchar(50) NOT NULL,
PRIMARY KEY (`language_pk`),
UNIQUE KEY `language_code` (`language_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `languages` VALUES
('lang001', 'en', 'English'),
('lang002', 'da', 'Danish'),
('lang003', 'es', 'Spanish'),
('lang004', 'fr', 'French');



CREATE TABLE IF NOT EXISTS `trends` (
`trend_pk` char(32) NOT NULL,
`trend_title` varchar(100) NOT NULL,
`trend_message` varchar(100) NOT NULL,
PRIMARY KEY (`trend_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `trends` VALUES
('t001', 'New Launch', 'A new rocket has been sent to the moon'),
('t002', 'Politics are Rotten', 'Everyone talks, few act'),
('t003', 'Tech Innovations', 'AI is taking over many tasks'),
('t004', 'Social Media Buzz', 'New app goes viral overnight');

COMMIT;
