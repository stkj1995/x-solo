-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 27. 11 2025 kl. 21:20:05
-- Serverversion: 10.6.20-MariaDB-ubu2004
-- PHP-version: 8.2.27

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

DELIMITER $$
--
-- Procedurer
--
CREATE DEFINER=`root`@`%` PROCEDURE `add_post` (IN `userID` CHAR(32), IN `message` VARCHAR(280), IN `imagePath` VARCHAR(255))   BEGIN
  INSERT INTO posts(post_pk, post_user_fk, post_message, post_image_path, post_total_likes)
  VALUES (UUID(), userID, message, imagePath, 0);
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `follow_user` (IN `followerID` CHAR(32), IN `targetID` CHAR(32))   BEGIN
  INSERT INTO follows(follow_pk, follow_user_fk, follow_target_fk)
  VALUES (UUID(), followerID, targetID);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `comments`
--

CREATE TABLE `comments` (
  `comment_pk` char(32) NOT NULL,
  `comment_post_fk` char(32) NOT NULL,
  `comment_user_fk` char(32) NOT NULL,
  `comment_message` varchar(255) NOT NULL,
  `comment_created_at` bigint(20) UNSIGNED NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `comments`
--

INSERT INTO `comments` (`comment_pk`, `comment_post_fk`, `comment_user_fk`, `comment_message`, `comment_created_at`, `created_at`) VALUES
('c001', 'p001', 'u002', 'Nice post!', 1700000100, '2025-11-27 13:01:44'),
('c002', 'p001', 'u003', 'I agree!', 1700000200, '2025-11-27 13:01:44'),
('c003', 'p002', 'u001', 'Welcome!', 1700000300, '2025-11-27 13:01:44'),
('c004', 'p004', 'u004', 'Cool update!', 1700000400, '2025-11-27 13:01:44'),
('c005', 'p005', 'u001', 'Congrats!', 1700000500, '2025-11-27 13:01:44'),
('c006', 'p006', 'u003', 'Good morning!', 1700000600, '2025-11-27 13:01:44');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `follows`
--

CREATE TABLE `follows` (
  `follow_pk` char(32) NOT NULL,
  `follow_user_fk` char(32) NOT NULL,
  `follow_target_fk` char(32) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `follows`
--

INSERT INTO `follows` (`follow_pk`, `follow_user_fk`, `follow_target_fk`, `created_at`) VALUES
('f001', 'u001', 'u002', '2025-11-27 13:01:44'),
('f002', 'u003', 'u001', '2025-11-27 13:01:44'),
('f003', 'u004', 'u001', '2025-11-27 13:01:44'),
('f004', 'u005', 'u002', '2025-11-27 13:01:44'),
('f005', 'u006', 'u003', '2025-11-27 13:01:44');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `languages`
--

CREATE TABLE `languages` (
  `language_pk` char(32) NOT NULL,
  `language_code` varchar(10) NOT NULL,
  `language_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `languages`
--

INSERT INTO `languages` (`language_pk`, `language_code`, `language_name`) VALUES
('lang001', 'en', 'English'),
('lang002', 'da', 'Danish'),
('lang003', 'es', 'Spanish'),
('lang004', 'fr', 'French');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `likes`
--

CREATE TABLE `likes` (
  `like_pk` char(32) NOT NULL,
  `like_post_fk` char(32) NOT NULL,
  `like_user_fk` char(32) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `likes`
--

INSERT INTO `likes` (`like_pk`, `like_post_fk`, `like_user_fk`, `created_at`) VALUES
('l001', 'p001', 'u002', '2025-11-27 13:01:44'),
('l002', 'p002', 'u001', '2025-11-27 13:01:44'),
('l003', 'p003', 'u004', '2025-11-27 13:01:44'),
('l004', 'p004', 'u001', '2025-11-27 13:01:44'),
('l005', 'p005', 'u003', '2025-11-27 13:01:44'),
('l006', 'p006', 'u005', '2025-11-27 13:01:44'),
('l007', 'p007', 'u006', '2025-11-27 13:01:44');

--
-- Triggers/udløsere `likes`
--
DELIMITER $$
CREATE TRIGGER `after_like_delete` AFTER DELETE ON `likes` FOR EACH ROW BEGIN
  UPDATE posts 
  SET post_total_likes = post_total_likes - 1
  WHERE post_pk = OLD.like_post_fk;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_like_insert` AFTER INSERT ON `likes` FOR EACH ROW BEGIN
  UPDATE posts 
  SET post_total_likes = post_total_likes + 1
  WHERE post_pk = NEW.like_post_fk;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Stand-in-struktur for visning `most_liked_posts`
-- (Se nedenfor for det aktuelle view)
--
CREATE TABLE `most_liked_posts` (
`post_pk` char(32)
,`post_message` varchar(280)
,`post_total_likes` bigint(20) unsigned
);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` varchar(10) DEFAULT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `post_image_path` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`, `created_at`) VALUES
('p001', 'u002', 'Hello world!', 0, 'post_1.jpg', '2025-11-27 13:01:44'),
('p002', 'u002', 'My first post', 0, '', '2025-11-27 13:01:44'),
('p003', 'u003', 'Testing posts', 0, 'post_2.jpg', '2025-11-27 13:01:44'),
('p004', 'u002', 'Another day, another post', 0, '', '2025-11-27 13:01:44'),
('p005', 'u004', 'Excited to join!', 0, 'post_3.jpg', '2025-11-27 13:01:44'),
('p006', 'u005', 'Good morning everyone', 0, '', '2025-11-27 13:01:44'),
('p007', 'u006', 'Loving this platform', 0, 'post_4.jpg', '2025-11-27 13:01:44');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `trends`
--

CREATE TABLE `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `trends`
--

INSERT INTO `trends` (`trend_pk`, `trend_title`, `trend_message`) VALUES
('t001', 'New Launch', 'A new rocket has been sent to the moon'),
('t002', 'Politics are Rotten', 'Everyone talks, few act'),
('t003', 'Tech Update', 'New AI model released'),
('t004', 'Sports', 'Big game tonight');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `users`
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
  `user_verified_at` bigint(20) UNSIGNED NOT NULL,
  `user_role` enum('user','admin') NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`, `user_role`) VALUES
('u002', 'daniel@example.com', 'scrypt:hash2', 'daniel', 'Daniel', '', 'avatar_2.jpg', 'key123', 0, 'user'),
('u003', 'mille@example.com', 'scrypt:hash3', 'mille', 'Mille', '', 'avatar_3.jpg', 'key456', 0, 'user'),
('u004', 'anna@example.com', 'scrypt:hash4', 'anna', 'Anna', 'Larsen', 'avatar_4.jpg', '', 1700001000, 'user'),
('u005', 'max@example.com', 'scrypt:hash5', 'max', 'Max', '', 'avatar_5.jpg', '', 1700002000, 'user'),
('u006', 'lara@example.com', 'scrypt:hash6', 'lara', 'Lara', '', 'avatar_6.jpg', 'key789', 0, 'user'),
('u007', 'test@example.com', 'hash', 'testuser', 'Test', 'User', 'avatar.jpg', '', 1764249116, 'user'),
('u008', 'sophieteinvigkjer@gmail.com', 'pbkdf2:sha256:260000$2FDxPGYcRRNWpA9PAZk9yb$3fcacdb39049a56e20d8c4e0563192812d00a6c02bdb5f92b315a60b63ba3267', 'sophie', 'Sophie', 'Teinvig Kjer', 'https://avatar.iran.liara.run/public/40', '\"\"', 1, 'user'),
('u999', 'admin@example.com', 'scrypt:hashAdmin', 'admin', 'Super', 'Admin', 'avatar_admin.jpg', '', 1700000000, 'admin');

-- --------------------------------------------------------

--
-- Stand-in-struktur for visning `user_post_counts`
-- (Se nedenfor for det aktuelle view)
--
CREATE TABLE `user_post_counts` (
`user_username` varchar(20)
,`total_posts` bigint(21)
);

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_pk`),
  ADD KEY `idx_comment_post_fk` (`comment_post_fk`),
  ADD KEY `idx_comment_user_fk` (`comment_user_fk`);

--
-- Indeks for tabel `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follow_pk`),
  ADD UNIQUE KEY `unique_follow` (`follow_user_fk`,`follow_target_fk`),
  ADD KEY `idx_follow_target_fk` (`follow_target_fk`);

--
-- Indeks for tabel `languages`
--
ALTER TABLE `languages`
  ADD PRIMARY KEY (`language_pk`),
  ADD UNIQUE KEY `language_code` (`language_code`);

--
-- Indeks for tabel `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`like_pk`),
  ADD UNIQUE KEY `unique_like` (`like_post_fk`,`like_user_fk`),
  ADD KEY `idx_like_post_fk` (`like_post_fk`),
  ADD KEY `idx_like_user_fk` (`like_user_fk`);

--
-- Indeks for tabel `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD KEY `idx_post_user_fk` (`post_user_fk`);
ALTER TABLE `posts` ADD FULLTEXT KEY `post_message` (`post_message`);

--
-- Indeks for tabel `trends`
--
ALTER TABLE `trends`
  ADD PRIMARY KEY (`trend_pk`);

--
-- Indeks for tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_username` (`user_username`),
  ADD KEY `idx_verified_at` (`user_verified_at`);

-- --------------------------------------------------------

--
-- Struktur for visning `most_liked_posts`
--
DROP TABLE IF EXISTS `most_liked_posts`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `most_liked_posts`  AS SELECT `posts`.`post_pk` AS `post_pk`, `posts`.`post_message` AS `post_message`, `posts`.`post_total_likes` AS `post_total_likes` FROM `posts` ORDER BY `posts`.`post_total_likes` DESC ;

-- --------------------------------------------------------

--
-- Struktur for visning `user_post_counts`
--
DROP TABLE IF EXISTS `user_post_counts`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`%` SQL SECURITY DEFINER VIEW `user_post_counts`  AS SELECT `u`.`user_username` AS `user_username`, count(`p`.`post_pk`) AS `total_posts` FROM (`users` `u` left join `posts` `p` on(`u`.`user_pk` = `p`.`post_user_fk`)) GROUP BY `u`.`user_pk` ;

--
-- Begrænsninger for dumpede tabeller
--

--
-- Begrænsninger for tabel `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `fk_comments_post` FOREIGN KEY (`comment_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `fk_likes_post` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `fk_posts_user` FOREIGN KEY (`post_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
