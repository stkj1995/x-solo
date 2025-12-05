-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 05. 12 2025 kl. 12:25:44
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

CREATE DEFINER=`root`@`%` PROCEDURE `create_post` (IN `p_user_pk` CHAR(32), IN `p_message` VARCHAR(280), IN `p_image` VARCHAR(255))   BEGIN
  INSERT INTO posts(post_pk, post_user_fk, post_message, post_image_path, post_total_likes, created_at)
  VALUES(UUID(), p_user_pk, p_message, p_image, 0, NOW());
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `follow_user` (IN `followerID` CHAR(32), IN `targetID` CHAR(32))   BEGIN
  INSERT INTO follows(follow_pk, follow_user_fk, follow_target_fk)
  VALUES (UUID(), followerID, targetID);
END$$

CREATE DEFINER=`root`@`%` PROCEDURE `get_profile` (IN `p_user_pk` CHAR(32))   BEGIN
  SELECT * FROM users WHERE user_pk = p_user_pk;
  SELECT * FROM posts WHERE post_user_fk = p_user_pk ORDER BY created_at DESC;
  SELECT * FROM follows WHERE follow_target_fk = p_user_pk;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `admin`
--

CREATE TABLE `admin` (
  `admin_pk` char(32) NOT NULL,
  `admin_email` varchar(255) NOT NULL,
  `admin_password` varchar(255) NOT NULL,
  `admin_first_name` varchar(100) NOT NULL,
  `admin_last_name` varchar(100) NOT NULL,
  `admin_role` varchar(50) DEFAULT 'superadmin',
  `admin_created_at` datetime NOT NULL DEFAULT current_timestamp(),
  `admin_avatar_path` varchar(255) NOT NULL DEFAULT 'avatar_admin_placeholder.jpg'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `admin`
--

INSERT INTO `admin` (`admin_pk`, `admin_email`, `admin_password`, `admin_first_name`, `admin_last_name`, `admin_role`, `admin_created_at`, `admin_avatar_path`) VALUES
('a001', 'admin@example.com', 'scrypt:hashAdmin', 'Super', 'Admin', 'superadmin', '2025-11-29 12:15:34', 'avatar_admin.jpg');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `comments`
--

CREATE TABLE `comments` (
  `comment_pk` char(32) NOT NULL,
  `comment_post_fk` char(32) NOT NULL,
  `comment_user_fk` char(32) NOT NULL,
  `comment_message` varchar(255) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `comments`
--

INSERT INTO `comments` (`comment_pk`, `comment_post_fk`, `comment_user_fk`, `comment_message`, `created_at`) VALUES
('1ad9fe5649bc4c97b91aacc3217bf570', '4e0180d683f64f34a3acab709854e3b4', 'u008', 'this is one more', '2025-12-04 11:25:04'),
('1c1c316d427546979e69b34607c7dc06', 'ff81e236f1974a5a9364efbf2b896677', 'u008', 'Oh that\'s nice', '2025-12-04 13:05:25'),
('c001', 'p001', 'u002', 'Nice post!', '2025-11-27 13:01:44'),
('c002', 'p001', 'u003', 'I agree!', '2025-11-27 13:01:44'),
('c004', 'p004', 'u004', 'Cool update!', '2025-11-27 13:01:44'),
('c006', 'p006', 'u003', 'Good morning!', '2025-11-27 13:01:44'),
('c007', 'p003', 'u002', 'Testing works fine.', '2025-11-27 09:22:30'),
('c008', 'p005', 'u007', 'Excited to see more posts!', '2025-11-27 10:12:44'),
('c009', 'p006', 'u001', 'Hope everyone has a great day!', '2025-11-27 08:30:12'),
('c010', 'p007', 'u008', 'Loving this platform too!', '2025-11-27 11:45:50'),
('c011', 'p004', 'u002', 'Thanks for sharing!', '2025-11-27 13:10:20'),
('c012', 'p005', 'u003', 'Very helpful post.', '2025-11-27 13:12:33'),
('eac6babb3f4c45fea310839cbc4e1f6b', '7a74bb4cd669417785747d099d022cae', 'f32f0425e18b4f8dbc33f0eb51331fbf', 'iucsvdvvbuvdubnsnsi', '2025-12-04 12:47:51'),
('f60900f43e67435c808bd4fd4f2ab427', '4e0180d683f64f34a3acab709854e3b4', 'u008', 'this is a comment', '2025-12-04 11:24:58');

--
-- Triggers/udløsere `comments`
--
DELIMITER $$
CREATE TRIGGER `after_comment_delete` AFTER DELETE ON `comments` FOR EACH ROW BEGIN
  UPDATE posts
  SET post_total_comments = post_total_comments - 1
  WHERE post_pk = OLD.comment_post_fk;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `after_comment_insert` AFTER INSERT ON `comments` FOR EACH ROW BEGIN
  UPDATE posts
  SET post_total_comments = post_total_comments + 1
  WHERE post_pk = NEW.comment_post_fk;
END
$$
DELIMITER ;

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
('lang003', 'es', 'Spanish');

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
DELIMITER $$
CREATE TRIGGER `trg_after_like_delete` AFTER DELETE ON `likes` FOR EACH ROW UPDATE posts
SET post_total_likes = post_total_likes - 1
WHERE post_pk = OLD.like_post_fk
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `trg_after_like_insert` AFTER INSERT ON `likes` FOR EACH ROW UPDATE posts 
SET post_total_likes = post_total_likes + 1 
WHERE post_pk = NEW.like_post_fk
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
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `post_image_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `post_total_comments` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`, `created_at`, `post_total_comments`) VALUES
('4e0180d683f64f34a3acab709854e3b4', 'u008', 'yolo', 0, '', '2025-12-04 09:12:45', 2),
('7a74bb4cd669417785747d099d022cae', 'f32f0425e18b4f8dbc33f0eb51331fbf', 'gheoiofjv', 0, '', '2025-12-04 10:37:21', 1),
('ff81e236f1974a5a9364efbf2b896677', 'u008', 'A poster', 0, '343839ff7c2e4b79a3159ea56c194642_SoMe_salling_brnecirkel_-_bliv_medlem.png', '2025-12-01 13:22:58', 1),
('p001', 'u008', 'Hello world! I\'m such an oooold lady', 0, 'post_1.jpg', '2025-11-27 13:01:44', 0),
('p002', 'u002', 'My first post', 0, 'cake.webp', '2025-11-21 13:01:44', 0),
('p003', 'u003', 'Testing posts', 0, 'post_2.jpg', '2025-11-27 13:01:44', 0),
('p004', 'u002', 'Another day, another post', 2, 'autumn.png', '2025-11-27 13:01:44', 0),
('p005', 'u004', 'Excited to join!', 0, 'post_3.jpg', '2025-11-29 18:30:40', 0),
('p006', 'u005', 'Good morning everyone', 0, 'post_5.jpg', '2025-11-28 14:01:44', 0),
('p007', 'u006', 'Loving this platform', 6, 'post_4.jpg', '2025-11-27 13:01:44', 0),
('p008', 'u009', 'Just joined this platform!', 0, NULL, '2025-12-04 14:00:00', 0),
('p009', 'u010', 'Loving the new features here!', 2, NULL, '2025-12-02 14:05:00', 1),
('p010', 'u011', 'Anyone wants to collaborate on a project?', 0, NULL, '2025-12-04 15:07:49', 0),
('p011', 'admin001', 'Welcome!!', 0, 'coffeee.png', '2025-11-29 13:09:40', 0),
('p012', 'u003', 'Coffee is life ☕️', 3, 'coffeee.png', '2025-12-04 11:04:00', 1),
('p013', 'u004', 'Just finished my final exam!! 🎉', 5, NULL, '2025-11-01 12:14:20', 2),
('p014', 'u011', 'Looking for collaboration partners 👀', 1, NULL, '2025-11-03 13:50:11', 0),
('p015', 'u010', 'New coding setup installed today 🔥', 4, 'setup.jpg', '2025-12-04 14:26:41', 3),
('p016', 'u009', 'Snow is finally here ❄️', 2, 'snow.jpg', '2025-12-04 15:01:55', 0),
('p017', 'u008', 'Making dinner… wish me luck 😂', 0, NULL, '2025-11-04 15:18:38', 0),
('p018', 'u002', 'This platform is growing fast!', 7, NULL, '2025-12-02 15:25:10', 1),
('p019', 'u006', 'Running 10km today, let’s go 💪', 6, 'run.jpg', '2025-12-04 15:30:22', 2),
('p020', 'u005', 'Throwback to last summer ☀️', 3, 'summer.jpg', '2025-12-04 15:33:41', 0),
('p021', 'admin001', 'Remember to be kind online ❤️', 0, 'kindness.jpg', '2025-12-04 15:37:52', 0);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `trends`
--

CREATE TABLE `trends` (
  `trend_pk` char(32) NOT NULL,
  `trend_title` varchar(100) NOT NULL,
  `trend_message` varchar(255) NOT NULL,
  `trend_user_fk` char(32) DEFAULT NULL,
  `trend_image` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `trends`
--

INSERT INTO `trends` (`trend_pk`, `trend_title`, `trend_message`, `trend_user_fk`, `trend_image`, `is_active`, `created_at`) VALUES
('t001', 'New Launch', 'A new rocket has been sent to the moon', 'u001', 'rocket.png', 1, '2025-11-29 22:14:26'),
('t002', 'Politics are Rotten', 'Everyone talks, few act', 'u002', 'politics.png', 1, '2025-11-29 09:14:34'),
('t003', 'Tech Update', 'New AI model released', 'u003', 'ai.png', 1, '2025-11-29 12:50:26'),
('t004', 'Sports', 'Big game tonight', 'u001', 'sports.png', 1, '2025-11-29 12:14:00'),
('t005', 'Music Vibes', 'Check out the latest rap album drops!', 'u008', 'music.png', 1, '2025-12-04 09:12:45'),
('t006', 'Coding Marathon', 'Join the weekend hackathon!', 'u010', 'coding.png', 1, '2025-12-04 10:37:21'),
('t007', 'Healthy Living', '5 tips to stay fit this winter', 'u009', 'fitness.png', 1, '2025-12-04 11:05:12'),
('t008', 'Travel Diaries', 'Top 10 places to visit in 2026', 'u011', 'travel.png', 1, '2025-12-04 13:48:59'),
('t009', 'Movie Buzz', 'New sci-fi movie trailers released', 'u002', 'movies.png', 1, '2025-12-04 14:22:33'),
('t010', 'Food Craze', 'Viral pasta recipe takes over the internet', 'u003', 'pasta.png', 1, '2025-12-04 15:12:33'),
('t011', 'Winter Fashion', 'New coat trends dominating 2025', 'u004', 'fashion.png', 1, '2025-12-04 15:14:21'),
('t012', 'Gaming Hype', 'Massive update released in CyberQuest X', 'u006', 'gaming.png', 1, '2025-12-04 15:18:00'),
('t013', 'Pet Lovers', '10 cutest dog photos trending right now', 'u009', 'dogs.png', 1, '2025-12-04 15:20:42'),
('t014', 'Student Life', 'How to survive exams with less stress', 'u011', 'student.png', 1, '2025-12-04 15:33:19'),
('t015', 'Eco News', 'New climate agreement signed globally', 'u002', 'climate.png', 1, '2025-12-04 15:36:20');

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
  `reset_token` varchar(255) DEFAULT NULL,
  `reset_expiry` datetime DEFAULT NULL,
  `user_verification_key` char(32) DEFAULT NULL,
  `user_verified_at` bigint(20) UNSIGNED NOT NULL DEFAULT 0,
  `user_role` enum('user','admin') NOT NULL DEFAULT 'user',
  `user_language_fk` char(32) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `reset_token`, `reset_expiry`, `user_verification_key`, `user_verified_at`, `user_role`, `user_language_fk`, `is_deleted`) VALUES
('admin001', 'admin@example.com', 'scrypt:hashAdmin', 'superadmin', 'Super', 'Admin', 'avatar_admin.jpg', NULL, NULL, '\'\'', 1764421513, 'admin', NULL, 0),
('f32f0425e18b4f8dbc33f0eb51331fbf', 'soph1155@stud.ek.dk', 'scrypt:32768:8:1$AS75Y7b9DW3wNUo1$d19735a9cdfcfc7a2ad9c47377e646f3d7eaf70aca31437d2481b3008255adff64ca665a5ec4bc214095ee1f139042460cadbb0040ae1a88246db63ffe4640e4', 'Tester', 'Sopheren', 'Testing', 'hands.png', NULL, NULL, '', 1764707764, 'user', NULL, 0),
('t999', 't999@example.com', 'dummyhash', 'testuser999', 'Test', 'User', 'avatar_2.jpg', NULL, NULL, NULL, 0, 'user', NULL, 0),
('u001', 'u001@example.invalid', 'placeholder', 'user001', 'Amin', 'Jensen', 'avatar_7.jpg', NULL, NULL, '\'\'', 0, 'user', NULL, 0),
('u002', 'daniel@example.com', 'scrypt:hash2', 'daniel', 'Daniel', 'Gertsen', 'avatar_2.jpg', NULL, NULL, '1234567890abcdef1234567890abcdef', 0, 'user', NULL, 0),
('u003', 'mille@example.com', 'scrypt:hash3', 'mille', 'Mille', 'Sørensen', 'avatar_3.jpg', NULL, NULL, 'key456', 0, 'user', NULL, 0),
('u004', 'anna@example.com', 'scrypt:hash4', 'anna', 'Anna', 'Larsen', 'avatar_4.jpg', NULL, NULL, '\'\'', 1700001000, 'user', NULL, 0),
('u005', 'max@example.com', 'scrypt:hash5', 'max', 'Max', 'Eriksen', 'avatar_5.jpg', NULL, NULL, '\'\'', 1700002000, 'user', NULL, 0),
('u006', 'lara@example.com', 'scrypt:hash6', 'lara', 'Lara', 'Hansen', 'avatar_6.jpg', NULL, NULL, 'key789', 0, 'user', NULL, 0),
('u007', 'test@example.com', 'hash', 'testuser', 'Kirsten', 'Abel Knudsen', 'avatar.jpg', NULL, NULL, '\'\'', 1764249116, 'user', NULL, 1),
('u008', 'sophieteinvigkjer@gmail.com', 'scrypt:32768:8:1$E6C1XsNIuJRQr6p9$a3bc4f2e87c15f2f9889505012b5f07dcdbc9dbb4a3c11ff6e3c03a5c87463c7539ecd1678fc3473a55f60e0023322f17a7e52dfb96947d0841c8aab421a81b4', 'teinvig', 'Sophie', 'Teinvig Kjer', 'u008_leaves.png', NULL, NULL, '', 1764708165, 'user', NULL, 0),
('u009', 'lina@example.com', 'scrypt:hash7', 'lina', 'Lina', 'Nielsen', 'avatar_9.jpg', NULL, NULL, '', 0, 'user', NULL, 0),
('u010', 'jonas@example.com', 'scrypt:hash8', 'jonas', 'Jonas', 'Hansen', 'avatar_10.jpg', NULL, NULL, '', 0, 'user', NULL, 0),
('u011', 'emil@example.com', 'scrypt:hash9', 'emil', 'Emil', 'Olsen', 'avatar_11.jpg', NULL, NULL, '', 0, 'user', NULL, 0);

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
-- Indeks for tabel `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_pk`),
  ADD UNIQUE KEY `admin_email` (`admin_email`),
  ADD UNIQUE KEY `unique_admin_email` (`admin_email`);

--
-- Indeks for tabel `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_pk`),
  ADD KEY `idx_comment_post` (`comment_post_fk`),
  ADD KEY `idx_comment_user` (`comment_user_fk`);

--
-- Indeks for tabel `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follow_pk`),
  ADD UNIQUE KEY `unique_follow` (`follow_user_fk`,`follow_target_fk`),
  ADD KEY `idx_follow_target_fk` (`follow_target_fk`),
  ADD KEY `idx_follow_user` (`follow_user_fk`),
  ADD KEY `idx_follow_target` (`follow_target_fk`);

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
  ADD UNIQUE KEY `unique_like` (`like_user_fk`,`like_post_fk`),
  ADD KEY `idx_like_post` (`like_post_fk`),
  ADD KEY `idx_like_user` (`like_user_fk`);

--
-- Indeks for tabel `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD KEY `idx_post_total_likes` (`post_total_likes`),
  ADD KEY `idx_user_created_at` (`post_user_fk`,`created_at`);
ALTER TABLE `posts` ADD FULLTEXT KEY `post_message` (`post_message`);

--
-- Indeks for tabel `trends`
--
ALTER TABLE `trends`
  ADD PRIMARY KEY (`trend_pk`),
  ADD KEY `idx_trend_user_active` (`trend_user_fk`,`is_active`);

--
-- Indeks for tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_pk`),
  ADD UNIQUE KEY `user_email` (`user_email`),
  ADD UNIQUE KEY `user_username` (`user_username`),
  ADD KEY `idx_verified_at` (`user_verified_at`),
  ADD KEY `fk_user_language` (`user_language_fk`);

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
  ADD CONSTRAINT `fk_comment_post` FOREIGN KEY (`comment_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_comment_user` FOREIGN KEY (`comment_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_comments_post` FOREIGN KEY (`comment_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_comments_user` FOREIGN KEY (`comment_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `fk_follows_target` FOREIGN KEY (`follow_target_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_follows_user` FOREIGN KEY (`follow_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follow_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`follow_target_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `fk_likes_post` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_likes_user` FOREIGN KEY (`like_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrænsninger for tabel `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `fk_post_user` FOREIGN KEY (`post_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_posts_user` FOREIGN KEY (`post_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `trends`
--
ALTER TABLE `trends`
  ADD CONSTRAINT `trends_ibfk_1` FOREIGN KEY (`trend_user_fk`) REFERENCES `users` (`user_pk`);

--
-- Begrænsninger for tabel `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `fk_user_language` FOREIGN KEY (`user_language_fk`) REFERENCES `languages` (`language_pk`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
