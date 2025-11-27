-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Vært: mariadb
-- Genereringstid: 26. 11 2025 kl. 10:09:28
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

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `comments`
--

CREATE TABLE `comments` (
  `comment_pk` char(32) NOT NULL,
  `comment_post_fk` char(32) NOT NULL,
  `comment_user_fk` char(32) NOT NULL,
  `comment_message` varchar(280) NOT NULL,
  `comment_created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `comments`
--

INSERT INTO `comments` (`comment_pk`, `comment_post_fk`, `comment_user_fk`, `comment_message`, `comment_created_at`) VALUES
('c1a2b3d4e5f67890123456789abcdef0', '1700c7f5fb7147358e4b1cd7f6b1d368', '14ce310158ef4147a7314f57aecf6028', 'This is my first comment!', '2025-11-25 12:39:09');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `follows`
--

CREATE TABLE `follows` (
  `follow_pk` char(32) NOT NULL,
  `follow_follower_fk` char(32) NOT NULL,
  `follow_following_fk` char(32) NOT NULL,
  `follow_created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `follows`
--

INSERT INTO `follows` (`follow_pk`, `follow_follower_fk`, `follow_following_fk`, `follow_created_at`) VALUES
('a14da879d6234b61bb6cf15fa7ff9ef9', '14ce310158ef4147a7314f57aecf6028', '59ac8f8892bc45528a631d4415151f13', '2025-11-25 19:42:31'),
('f2b3c4d5e6f7890123456789abcdef01', '225a9fc15b8f409aa5c8ee7eafee516b', '14ce310158ef4147a7314f57aecf6028', '2025-11-25 13:15:00');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `languages`
--

CREATE TABLE `languages` (
  `id` int(11) NOT NULL,
  `key` varchar(255) NOT NULL,
  `english` varchar(255) NOT NULL,
  `danish` varchar(255) NOT NULL,
  `spanish` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `languages`
--

INSERT INTO `languages` (`id`, `key`, `english`, `danish`, `spanish`) VALUES
(1, 'login_title', 'Login', 'Log ind', 'Iniciar sesión'),
(2, 'signup_button', 'Sign up', 'Opret bruger', 'Registro'),
(3, 'email_label', 'Email', 'Email', 'Correo');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `likes`
--

CREATE TABLE `likes` (
  `like_pk` char(32) NOT NULL,
  `like_post_fk` char(32) NOT NULL,
  `like_user_fk` char(32) NOT NULL,
  `like_created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `likes`
--

INSERT INTO `likes` (`like_pk`, `like_post_fk`, `like_user_fk`, `like_created_at`) VALUES
('l1a2b3c4d5e67890123456789abcdef0', '1700c7f5fb7147358e4b1cd7f6b1d368', '14ce310158ef4147a7314f57aecf6028', '2025-11-25 13:30:00'),
('l2b3c4d5e6f7890123456789abcdef01', '1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', '2025-11-25 13:32:00'),
('l3c4d5e6f7a890123456789abcdef012', '28dd4c1671634d73acd29a0ab109bef5', '805a39cd8c854ee8a83555a308645bf5', '2025-11-25 13:35:00');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `posts`
--

CREATE TABLE `posts` (
  `post_pk` char(32) NOT NULL,
  `post_user_fk` char(32) NOT NULL,
  `post_message` varchar(280) NOT NULL,
  `post_total_likes` bigint(20) UNSIGNED NOT NULL,
  `post_image_path` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `posts`
--

INSERT INTO `posts` (`post_pk`, `post_user_fk`, `post_message`, `post_total_likes`, `post_image_path`, `created_at`) VALUES
('09a22c05a0cd4975b2c5bb1b2fdeb37b', '14ce310158ef4147a7314f57aecf6028', 'lioho', 0, '', '2025-11-25 09:23:49'),
('0b2634e415d949428c6e1dbfc0e8ade7', '14ce310158ef4147a7314f57aecf6028', 'ljnb', 0, '', '2025-11-25 11:21:41'),
('0b46eea867ff4f0d827cffe4095c0f94', '14ce310158ef4147a7314f57aecf6028', 'mklhbgv', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:32:49'),
('1700c7f5fb7147358e4b1cd7f6b1d368', '14ce310158ef4147a7314f57aecf6028', 'kk', 0, '', '2025-11-25 11:14:23'),
('1ccba555068a4aaabf3b99b6176d4771', '14ce310158ef4147a7314f57aecf6028', 'whats up', 0, '', '2025-11-25 09:23:49'),
('1e5ecc804e1f46bc8e723437bf4bfc4b', '225a9fc15b8f409aa5c8ee7eafee516b', 'And this just works!', 0, 'post_3.jpg', '2025-11-25 09:23:49'),
('23e6544d641e46b0a91e0adfee87bfc6', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-25 20:40:50'),
('240c2d2c8eee4705846fb65547c7e71a', '14ce310158ef4147a7314f57aecf6028', 'p¨åojigydkjhg', 0, '', '2025-11-25 09:23:49'),
('26e6f9afbb544bd7b077f641dad2f6ca', '14ce310158ef4147a7314f57aecf6028', 'cccvcc', 0, '', '2025-11-25 09:23:49'),
('28dd4c1671634d73acd29a0ab109bef5', '805a39cd8c854ee8a83555a308645bf5', 'My first super life !', 0, 'post_3.jpg', '2025-11-25 09:23:49'),
('2ce2bb9685674c5f8fbd76c3ce06cbce', '14ce310158ef4147a7314f57aecf6028', 'kihg', 0, '', '2025-11-25 10:19:46'),
('358f373bb706437bab4a8ce5820bed2b', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-25 20:51:51'),
('39c32e0021b54cdfa7c237024e2b7125', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1281.PNG', '2025-11-25 20:40:26'),
('4808e2fa12084ef59dd91f3c6a0ef905', '14ce310158ef4147a7314f57aecf6028', 'heelofihrbv', 0, '', '2025-11-25 09:23:49'),
('508fb1f6db8648b1af3cdcbb947d4b6b', '14ce310158ef4147a7314f57aecf6028', 'lkiugcxdf', 0, '', '2025-11-25 09:23:49'),
('53a6017f506f4d9aa48b2e1c4d706f47', '14ce310158ef4147a7314f57aecf6028', '', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:37:35'),
('5474085f3b2c47a6ab185cff13b6154a', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-26 09:51:38'),
('568ccf3f51d54283a9aa626588a58e9a', '14ce310158ef4147a7314f57aecf6028', 'hello', 0, '', '2025-11-25 09:23:49'),
('590e248d4af6474ab965737d41d2c47f', '14ce310158ef4147a7314f57aecf6028', 'lkjhg', 0, '', '2025-11-25 10:44:41'),
('6aad37c02924464598093c8bcaf09992', '14ce310158ef4147a7314f57aecf6028', 'hej med dig', 0, '', '2025-11-25 09:23:49'),
('78f1f82c2fc24b2ba6e2c771465d5f80', '14ce310158ef4147a7314f57aecf6028', 'mnbvkj', 0, '', '2025-11-25 11:19:22'),
('7b4323a14d6b4f0386f0e53154fb5b56', '14ce310158ef4147a7314f57aecf6028', 'hello monkey', 0, '', '2025-11-25 09:23:49'),
('84eb774c63794228a44e672136529120', '14ce310158ef4147a7314f57aecf6028', 'lkibkv yoikrf', 0, '', '2025-11-25 09:23:49'),
('86317315e2f34e0cb9a8470914810b77', '14ce310158ef4147a7314f57aecf6028', 'heelofihrbv', 0, '', '2025-11-25 09:23:49'),
('8dd86bc58dae4f10bd1304e9609b2e36', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1281.PNG', '2025-11-25 20:47:59'),
('981fb7043b774881a7a3344f8509e2cb', '14ce310158ef4147a7314f57aecf6028', 'hejmmcoiuhg', 0, '', '2025-11-25 10:50:55'),
('99b251cd5edc45d58a7368a822dc8713', '14ce310158ef4147a7314f57aecf6028', '', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:36:37'),
('9a3aef3fe2154cc4bf8bf7840072d868', '14ce310158ef4147a7314f57aecf6028', 'klmbgfc', 0, '/static/uploads/babymad.jpeg', '2025-11-25 20:27:23'),
('9b95fb8f50734ec196b4782b23412544', '14ce310158ef4147a7314f57aecf6028', 'heeellopouiyt', 0, '', '2025-11-25 09:23:49'),
('a74b38d8168644bf964f1d41207e4ea6', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-25 20:45:31'),
('aa95d8a6f0f4410cbdc191cc26fbb792', '14ce310158ef4147a7314f57aecf6028', 'lkjmn', 0, '', '2025-11-25 19:59:42'),
('abaa00b0dd0a4c4d9f1ea2e22162cce9', '14ce310158ef4147a7314f57aecf6028', 'poiuytohgf', 0, '', '2025-11-25 10:23:29'),
('bd5a91ba2e5a4af69fd8d3626563d224', '14ce310158ef4147a7314f57aecf6028', 'jkojj', 0, '', '2025-11-25 11:30:21'),
('c42787d9ceeb478e8e4a943ed65b687d', '14ce310158ef4147a7314f57aecf6028', '', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:37:12'),
('ceaf77da835a4e99b7397e40409830df', '14ce310158ef4147a7314f57aecf6028', 'poiuhygfds', 0, '', '2025-11-25 09:23:49'),
('d05506dc197c477eaa5caaeeb89ea996', '14ce310158ef4147a7314f57aecf6028', 'kljnhvc', 0, '/static/uploads/IMG_1281.PNG', '2025-11-25 20:28:38'),
('d35c96d4ab934c42a5b4f0af29573b9a', '14ce310158ef4147a7314f57aecf6028', 'lkhbvlkjhg', 0, '', '2025-11-25 10:24:08'),
('d5ad0b5fc828420a9798b003fa37ac5c', '14ce310158ef4147a7314f57aecf6028', 'pokjh', 0, '', '2025-11-25 09:23:49'),
('da264137b3684365afe3b9a6a7e469e6', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-25 20:44:31'),
('db3a3af6003e4692bacb39b04545664c', '14ce310158ef4147a7314f57aecf6028', 'hej', 0, '', '2025-11-25 09:23:49'),
('dbf39d9529a84ae48b81ff558d67052a', '14ce310158ef4147a7314f57aecf6028', 'heelofihrbv ijg', 0, '', '2025-11-25 09:23:49'),
('dd240b389bee4116bfda94f0e7019028', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-25 20:43:21'),
('de9c71b9e4f54284903b9309c2d75597', '14ce310158ef4147a7314f57aecf6028', 'hello', 0, '', '2025-11-25 09:23:49'),
('e1b13c8f121a4cc6810b51bdc268ceb7', '14ce310158ef4147a7314f57aecf6028', '', 0, 'uploads/IMG_1235.PNG', '2025-11-26 10:01:55'),
('e35563da548344a0bc81ef8fdead2bf7', '14ce310158ef4147a7314f57aecf6028', '', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:34:43'),
('e78845836b7b417aa851bd85b4a19ca1', '14ce310158ef4147a7314f57aecf6028', 'kjhgf', 0, '', '2025-11-25 10:18:29'),
('ee4434e82768413d81c65aa4252303c7', '14ce310158ef4147a7314f57aecf6028', 'test', 0, '', '2025-11-25 09:23:49'),
('f8829be3f109423ea3e6bb0489c6afdc', '14ce310158ef4147a7314f57aecf6028', 'æopiiuyt', 0, '', '2025-11-25 09:23:49');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `post_trends`
--

CREATE TABLE `post_trends` (
  `post_pk` char(32) NOT NULL,
  `trend_pk` char(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
('6543c995d1af4ebcbd5280a4afaa1e2c', 'Politics are rotten', 'Everyone talks and only a few try to do something'),
('8343c995d1af4ebcbd5280a6afaa1e2d', 'New rocket to the moon', 'A new rocket has been sent towards the moon, but id didn\'t make it');

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
  `user_verified_at` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `users`
--

INSERT INTO `users` (`user_pk`, `user_email`, `user_password`, `user_username`, `user_first_name`, `user_last_name`, `user_avatar_path`, `user_verification_key`, `user_verified_at`) VALUES
('14ce310158ef4147a7314f57aecf6028', 'sophieteinvigkjer@gmail.com', 'scrypt:32768:8:1$Ps10nrNk2H13dS5A$eab208b22e6781797c116e23c957bb0293633d21b160f894b218afcb3be17a5d9784c1d2d8c51df812f04f71fba5bba6cb8f27208460fc3ccb9cbcfd4a162850', 'teinvig', 'sophie', '', 'https://avatar.iran.liara.run/public/40', '', 1763902862),
('21e66977ccb74fdbb6cbdb3e7e3a12cb', 'daniel@gmail.com', 'hashedpassword1', 'daniel', 'Daniel', '', 'avatar_2.jpg', 'c29fa5894f224964953801c925a7cac5', 0),
('225a9fc15b8f409aa5c8ee7eafee516b', 'a@aaa.com', 'hashedpassword2', 'santisss', 'Tester', '', 'avatar_1.jpg', '', 455656),
('59ac8f8892bc45528a631d4415151f13', 'terese@gmail.com', 'hashedpassword3', 'Mily', 'Mille', '', '', '', 45665656),
('6b48c6095913402eb4841529830e5415', 'a@a.com', 'hashedpassword4', 'Sofi', 'Sofie', '', '', '', 45445),
('805a39cd8c854ee8a83555a308645bf5', 'fullflaskdemomail@gmail.com', 'hashedpassword5', 'santiago', 'Santiago', '', 'avatar_3.jpg', '', 565656),
('88a93bb5267e443eb0047f421a7a2f34', 'santi@gmail.com', 'hashedpassword6', 'gustav', 'Gustav', '', 'avatar_2.jpg', '', 54654564);

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `user_follows`
--

CREATE TABLE `user_follows` (
  `follow_pk` char(32) NOT NULL,
  `follower_fk` char(32) NOT NULL,
  `following_fk` char(32) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Data dump for tabellen `user_follows`
--

INSERT INTO `user_follows` (`follow_pk`, `follower_fk`, `following_fk`, `created_at`) VALUES
('653167d912134486a1aab19c7e5e04f2', '14ce310158ef4147a7314f57aecf6028', '88a93bb5267e443eb0047f421a7a2f34', '2025-11-25 13:10:26'),
('e7889b59dcd44322a1e7182872a83962', '14ce310158ef4147a7314f57aecf6028', '59ac8f8892bc45528a631d4415151f13', '2025-11-25 13:10:30');

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `user_languages`
--

CREATE TABLE `user_languages` (
  `user_pk` char(32) NOT NULL,
  `language_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_pk`),
  ADD KEY `fk_comments_post` (`comment_post_fk`),
  ADD KEY `fk_comments_user` (`comment_user_fk`);

--
-- Indeks for tabel `follows`
--
ALTER TABLE `follows`
  ADD PRIMARY KEY (`follow_pk`),
  ADD KEY `fk_follows_follower` (`follow_follower_fk`),
  ADD KEY `fk_follows_following` (`follow_following_fk`);

--
-- Indeks for tabel `languages`
--
ALTER TABLE `languages`
  ADD PRIMARY KEY (`id`);

--
-- Indeks for tabel `likes`
--
ALTER TABLE `likes`
  ADD PRIMARY KEY (`like_pk`),
  ADD KEY `fk_likes_post` (`like_post_fk`),
  ADD KEY `fk_likes_user` (`like_user_fk`);

--
-- Indeks for tabel `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`post_pk`),
  ADD KEY `fk_posts_user` (`post_user_fk`);

--
-- Indeks for tabel `post_trends`
--
ALTER TABLE `post_trends`
  ADD PRIMARY KEY (`post_pk`,`trend_pk`),
  ADD KEY `trend_pk` (`trend_pk`);

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
  ADD UNIQUE KEY `user_name` (`user_username`);

--
-- Indeks for tabel `user_follows`
--
ALTER TABLE `user_follows`
  ADD PRIMARY KEY (`follow_pk`),
  ADD UNIQUE KEY `follower_fk` (`follower_fk`,`following_fk`),
  ADD KEY `following_fk` (`following_fk`);

--
-- Indeks for tabel `user_languages`
--
ALTER TABLE `user_languages`
  ADD PRIMARY KEY (`user_pk`,`language_id`),
  ADD KEY `language_id` (`language_id`);

--
-- Brug ikke AUTO_INCREMENT for slettede tabeller
--

--
-- Tilføj AUTO_INCREMENT i tabel `languages`
--
ALTER TABLE `languages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Begrænsninger for dumpede tabeller
--

--
-- Begrænsninger for tabel `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `fk_comments_post` FOREIGN KEY (`comment_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_comments_user` FOREIGN KEY (`comment_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrænsninger for tabel `follows`
--
ALTER TABLE `follows`
  ADD CONSTRAINT `fk_follow_follower` FOREIGN KEY (`follow_follower_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_follow_following` FOREIGN KEY (`follow_following_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_follows_follower` FOREIGN KEY (`follow_follower_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_follows_following` FOREIGN KEY (`follow_following_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrænsninger for tabel `likes`
--
ALTER TABLE `likes`
  ADD CONSTRAINT `fk_like_post` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_like_user` FOREIGN KEY (`like_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_likes_post` FOREIGN KEY (`like_post_fk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_likes_user` FOREIGN KEY (`like_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrænsninger for tabel `posts`
--
ALTER TABLE `posts`
  ADD CONSTRAINT `fk_post_user` FOREIGN KEY (`post_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_posts_user` FOREIGN KEY (`post_user_fk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Begrænsninger for tabel `post_trends`
--
ALTER TABLE `post_trends`
  ADD CONSTRAINT `post_trends_ibfk_1` FOREIGN KEY (`post_pk`) REFERENCES `posts` (`post_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `post_trends_ibfk_2` FOREIGN KEY (`trend_pk`) REFERENCES `trends` (`trend_pk`) ON DELETE CASCADE;

--
-- Begrænsninger for tabel `user_follows`
--
ALTER TABLE `user_follows`
  ADD CONSTRAINT `user_follows_ibfk_1` FOREIGN KEY (`follower_fk`) REFERENCES `users` (`user_pk`),
  ADD CONSTRAINT `user_follows_ibfk_2` FOREIGN KEY (`following_fk`) REFERENCES `users` (`user_pk`);

--
-- Begrænsninger for tabel `user_languages`
--
ALTER TABLE `user_languages`
  ADD CONSTRAINT `user_languages_ibfk_1` FOREIGN KEY (`user_pk`) REFERENCES `users` (`user_pk`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_languages_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `languages` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
