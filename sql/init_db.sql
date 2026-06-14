DROP DATABASE IF EXISTS link_swipe;

CREATE DATABASE link_swipe
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE link_swipe;

-- 1. 카테고리 테이블
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. 사용자 테이블
CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NULL,
    nickname VARCHAR(50) NOT NULL,
    provider VARCHAR(20) NOT NULL DEFAULT 'local',
    google_sub VARCHAR(255) UNIQUE NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 콘텐츠 보관함 테이블
CREATE TABLE contents (
    content_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    category_id INT,
    original_url TEXT NOT NULL,
    title VARCHAR(500) NOT NULL,
    video_id VARCHAR(100),
    channel_name VARCHAR(255),
    thumbnail_url TEXT,
    ai_summary TEXT,
    platform_type VARCHAR(50),
    status ENUM('unread', 'read', 'reread') DEFAULT 'unread',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_contents_user FOREIGN KEY (user_id)
        REFERENCES users(user_id) ON DELETE CASCADE,

    CONSTRAINT fk_contents_category FOREIGN KEY (category_id)
        REFERENCES categories(category_id) ON DELETE SET NULL
);

-- 기본 카테고리 데이터
INSERT INTO categories (name) VALUES
('자기계발'),
('운동'),
('요리'),
('여행'),
('뉴스'),
('콘텐츠'),
('기타');