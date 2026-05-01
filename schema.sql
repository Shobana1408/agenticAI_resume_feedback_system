CREATE DATABASE IF NOT EXISTS agentic_resume_db;
USE agentic_resume_db;

CREATE TABLE IF NOT EXISTS analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255),
    target_role VARCHAR(255),
    filename VARCHAR(255),
    ats_score INT,
    matched_skills TEXT,
    missing_skills TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);