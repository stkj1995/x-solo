-- --------------------------------------------------------
-- DATABASE SETUP
-- --------------------------------------------------------
CREATE DATABASE IF NOT EXISTS x;
USE x;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- --------------------------------------------------------
-- TABLE: users
-- --------------------------------------------------------
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
  UNIQUE KEY `user_name` (`user_username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: posts
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `post_image_path` varchar(255) NOT NULL,
  PRIMARY KEY (`post_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: comments
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `comments` (
  `comment_pk` char(32) NOT NULL,
  `comment_post_fk` char(32) NOT NULL,
  `comment_user_fk` char(32) NOT NULL,
  `comment_message` varchar(255) NOT NULL,
  `comment_created_at` bigint(20) UNSIGNED NOT NULL,
  PRIMARY KEY (`comment_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: follows
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `follows` (
  `follow_pk` char(32) NOT NULL,
  `follow_user_fk` char(32) NOT NULL,
  `follow_target_fk` char(32) NOT NULL,
  PRIMARY KEY (`follow_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: likes
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `likes` (
  `like_pk` char(32) NOT NULL,
  `like_post_fk` char(32) NOT NULL,
  `like_user_fk` char(32) NOT NULL,
  PRIMARY KEY (`like_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: languages
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `languages` (
  `language_pk` char(32) NOT NULL,
  `language_code` varchar(10) NOT NULL,
  `language_name` varchar(50) NOT NULL,
  PRIMARY KEY (`language_pk`),
  UNIQUE KEY `language_code` (`language_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- TABLE: trends
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL,
  PRIMARY KEY (`trend_pk`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- OPTIONAL: insert test users
-- --------------------------------------------------------
INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`) VALUES
('225a9fc15b8f409aa5c8ee7eafee516b', 'a@aaa.com', 'scrypt:32768:8:1$example$hash', 'tester', 'Test', '', 'avatar_1.jpg', '', 455656),
('59ac8f8892bc45528a631d4415151f13', 'terese@gmail.com', 'scrypt:32768:8:1$example$hash', 'Mily', 'Mille', '', '', '', 45665656);
