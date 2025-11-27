-- ##############################
-- DATABASE: x
-- ##############################

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------
-- Drop tables if they exist
-- --------------------------
DROP TABLE IF EXISTS follows;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS trends;
DROP TABLE IF EXISTS languages;

-- --------------------------
-- Create users table
-- --------------------------
CREATE TABLE users (
    user_pk VARCHAR(32) PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create follows table
-- --------------------------
CREATE TABLE follows (
    follower_id VARCHAR(32) NOT NULL,
    followee_id VARCHAR(32) NOT NULL,
    PRIMARY KEY (follower_id, followee_id),
    FOREIGN KEY (follower_id) REFERENCES users(user_pk) ON DELETE CASCADE,
    FOREIGN KEY (followee_id) REFERENCES users(user_pk) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create posts table
-- --------------------------
CREATE TABLE posts (
    post_pk CHAR(32) NOT NULL,
    post_user_fk CHAR(32) NOT NULL,
    post_message VARCHAR(280) NOT NULL,
    post_total_likes BIGINT(20) UNSIGNED NOT NULL,
    post_image_path VARCHAR(255) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY (post_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create comments table
-- --------------------------
CREATE TABLE comments (
    comment_pk CHAR(32) NOT NULL,
    comment_post_fk CHAR(32) NOT NULL,
    comment_user_fk CHAR(32) NOT NULL,
    comment_message VARCHAR(280) NOT NULL,
    comment_created_at TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY (comment_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create likes table
-- --------------------------
CREATE TABLE likes (
    like_pk CHAR(32) NOT NULL,
    like_post_fk CHAR(32) NOT NULL,
    like_user_fk CHAR(32) NOT NULL,
    like_created_at TIMESTAMP NOT NULL DEFAULT current_timestamp(),
    PRIMARY KEY (like_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create trends table
-- --------------------------
CREATE TABLE trends (
    trend_pk CHAR(32) NOT NULL,
    trend_title VARCHAR(100) NOT NULL,
    trend_total_posts BIGINT(20) UNSIGNED NOT NULL DEFAULT 0,
    PRIMARY KEY (trend_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------
-- Create languages table
-- --------------------------
CREATE TABLE languages (
    id INT(11) NOT NULL,
    `key` VARCHAR(255) NOT NULL,
    english VARCHAR(255) NOT NULL,
    danish VARCHAR(255) NOT NULL,
    spanish VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ##############################
-- Insert users
-- ##############################
INSERT INTO users (user_pk, name, email, password) VALUES
('u1', 'Sophie', 'sophieteinvigkjer@gmail.com', 'hashedpassword1'),
('u2', 'Alice', 'alice@example.com', 'hashedpassword2'),
('u3', 'Bob', 'bob@example.com', 'hashedpassword3'),
('u4', 'Charlie', 'charlie@example.com', 'hashedpassword4'),
('u5', 'David', 'david@example.com', 'hashedpassword5'),
('u6', 'Eva', 'eva@example.com', 'hashedpassword6'),
('u7', 'Frank', 'frank@example.com', 'hashedpassword7'),
('u8', 'Grace', 'grace@example.com', 'hashedpassword8'),
('u9', 'Hannah', 'hannah@example.com', 'hashedpassword9'),
('u10', 'Ian', 'ian@example.com', 'hashedpassword10'),
('u11', 'Julia', 'julia@example.com', 'hashedpassword11');

-- ##############################
-- Insert follows
-- ##############################
INSERT INTO follows (follower_id, followee_id) VALUES
('u1', 'u2'), ('u1', 'u3'), ('u1', 'u4'),
('u2', 'u1'), ('u2', 'u3'),
('u3', 'u1'), ('u3', 'u5'),
('u4', 'u1'), ('u4', 'u6'),
('u5', 'u2'), ('u5', 'u7'),
('u6', 'u3'), ('u6', 'u8'),
('u7', 'u4'), ('u7', 'u9'),
('u8', 'u5'), ('u8', 'u10'),
('u9', 'u6'), ('u9', 'u11'),
('u10', 'u7'), ('u10', 'u1'),
('u11', 'u8'), ('u11', 'u2');

-- ##############################
-- Insert posts
-- ##############################
INSERT INTO posts (post_pk, post_user_fk, post_message, post_total_likes, post_image_path, created_at) VALUES
('09a22c05a0cd4975b2c5bb1b2fdeb37b', 'u1', 'lioho', 0, '', '2025-11-25 09:23:49'),
('0b2634e415d949428c6e1dbfc0e8ade7', 'u1', 'ljnb', 0, '', '2025-11-25 11:21:41'),
('0b46eea867ff4f0d827cffe4095c0f94', 'u1', 'mklhbgv', 0, '/static/uploads/IMG_1235.PNG', '2025-11-25 20:32:49'),
('1700c7f5fb7147358e4b1cd7f6b1d368', 'u1', 'kk', 0, '', '2025-11-25 11:14:23'),
('1e5ecc804e1f46bc8e723437bf4bfc4b', 'u2', 'And this just works!', 0, 'post_3.jpg', '2025-11-25 09:23:49'),
('28dd4c1671634d73acd29a0ab109bef5', 'u3', 'My first super life !', 0, 'post_3.jpg', '2025-11-25 09:23:49');

-- ##############################
-- Insert comments
-- ##############################
INSERT INTO comments (comment_pk, comment_post_fk, comment_user_fk, comment_message, comment_created_at) VALUES
('c1a2b3d4e5f67890123456789abcdef0', '1700c7f5fb7147358e4b1cd7f6b1d368', 'u1', 'This is my first comment!', '2025-11-25 12:39:09');

-- ##############################
-- Insert likes
-- ##############################
INSERT INTO likes (like_pk, like_post_fk, like_user_fk, like_created_at) VALUES
('l1a2b3c4d5e67890123456789abcdef0', '1700c7f5fb7147358e4b1cd7f6b1d368', 'u1', '2025-11-25 13:30:00'),
('l2b3c4d5e6f7890123456789abcdef01', '1e5ecc804e1f46bc8e723437bf4bfc4b', 'u2', '2025-11-25 13:32:00'),
('l3c4d5e6f7a890123456789abcdef012', '28dd4c1671634d73acd29a0ab109bef5', 'u3', '2025-11-25 13:35:00');

-- ##############################
-- Insert trends
-- ##############################
INSERT INTO trends (trend_pk, trend_title, trend_total_posts) VALUES
('a1', 'fashion', 15),
('b2', 'coding', 8);

-- ##############################
-- Insert languages
-- ##############################
INSERT INTO languages (id, `key`, english, danish, spanish) VALUES
(1, 'login_title', 'Login', 'Log ind', 'Iniciar sesión'),
(2, 'signup_button', 'Sign up', 'Opret bruger', 'Registro'),
(3, 'email_label', 'Email', 'Email', 'Correo');

COMMIT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
