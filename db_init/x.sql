-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Generation Time: Nov 03, 2025 at 10:58 PM
-- Server version: 10.6.20-MariaDB-ubu2004
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `x`
--

-- --------------------------------------------------------

-- DROPPING TABLES IF THEY ALREADY EXIST --
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS trends;

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL,
  `post_image_path` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `comments` AND indexing
--

CREATE TABLE `comments` (
  `comment_pk`        char(32)      NOT NULL,
  `comment_text`      varchar(255)  NOT NULL,
  `post_fk`           char(32)      NOT NULL,
  `user_fk`           char(32)      NOT NULL,
  `comment_created_at` datetime     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (`comment_pk`),
  KEY `post_fk` (`post_fk`),
  KEY `user_fk` (`user_fk`)
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`) VALUES
('1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', 'Example tweet 01', 0, 'post_3.jpg'),
('258aeac7242348058c8c36f025b10fd5', '225a9fc15b8f409aa5c8ee7eafee516b', 'Example tweet 02', 0, '');

-- --------------------------------------------------------

--
-- Table structure for table `trends`
--

CREATE TABLE `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trends`
--

INSERT INTO `trends` (`trend_pk`, `trend_title`, `trend_message`) VALUES
('6543c995d1af4ebcbd5280a4afaa1e2c', 'Example trend 01', 'Everyone talks and only a few try to do something'),
('8343c995d1af4ebcbd5280a6afaa1e2d', 'Example trend 02', 'A new rocket has been sent towards the moon, but id didn\'t make it');


INSERT INTO `comments` (`comment_pk`, `comment_text`, `post_fk`, `user_fk`, `comment_created_at`) VALUES
('40653f3138fa4ea8-8ca0aa029359740b', 'Example comment 01', '1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', '2025-11-26 12:30:42'),
('549835b3b685476b-956bea95acd89c90', 'Example comment 02', '1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', '2025-11-26 12:30:42');
-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_pk` char(32) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_username` varchar(20) NOT NULL,
  `user_first_name` varchar(20) NOT NULL,
  `user_last_name` varchar(20) NOT NULL DEFAULT '',
  `user_avatar_path` varchar(50) NOT NULL,
  `user_verification_key` char(32) NOT NULL,
  `user_verified_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`) VALUES
('225a9fc15b8f409aa5c8ee7eafee516b', 'first@user.com', 'scrypt:32768:8:1$wnse70hQwhCvR9tC$724c32a91b5f277201afbb141f9293a93168327df5c9124f482d3c32b8dff991c41629f477dfaee021965f9b15318a4257aad2e933101a4c998ef3c346fc84e4', 'First', 'Userson', '', 'avatar_1.jpg', '', 455656),
('a063aedfefc64a4c9723f30cb9384586', 'test@user.com', 'scrypt:32768:8:1$ROylnHWuYjvIGG44$bd26f236301fc17ccd1d4d196b5b212290017826a75709c194505d4760047b955f536f58894a5221d8846a67a71c354536dffda75ebe5bdf1adde99dbfa3a33d', 'Test', 'Userson', '', 'avatar_2.jpg', '', 455656);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD UNIQUE KEY `post_pk` (`post_pk`);

--
-- Indexes for table `trends`
--
ALTER TABLE `trends`
  ADD UNIQUE KEY `trend_pk` (`trend_pk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_pk` (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_name` (`user_username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
