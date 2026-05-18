-- Crop Disease Detection System - Database Schema
-- MySQL 8+

CREATE DATABASE IF NOT EXISTS crop_disease_db;
USE crop_disease_db;

CREATE TABLE IF NOT EXISTS users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('farmer', 'admin') DEFAULT 'farmer',
    phone VARCHAR(20),
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS diseases (
    disease_id INT PRIMARY KEY AUTO_INCREMENT,
    disease_name VARCHAR(100) NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    description TEXT,
    symptoms TEXT,
    causes TEXT,
    treatment TEXT,
    prevention TEXT,
    severity_level ENUM('low', 'medium', 'high') DEFAULT 'medium',
    UNIQUE KEY uk_disease (disease_name)
);

CREATE TABLE IF NOT EXISTS predictions (
    prediction_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    predicted_disease VARCHAR(100) NOT NULL,
    confidence_score DECIMAL(5,2) NOT NULL,
    crop_type VARCHAR(50) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('detected', 'healthy') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detection_history (
    history_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    prediction_id INT NOT NULL,
    feedback TEXT,
    accuracy_rating INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS model_metrics (
    metric_id INT PRIMARY KEY AUTO_INCREMENT,
    model_version VARCHAR(20) DEFAULT '1.0',
    accuracy DECIMAL(5,2) NOT NULL,
    precision_score DECIMAL(5,2) NOT NULL,
    recall_score DECIMAL(5,2) NOT NULL,
    f1_score DECIMAL(5,2) NOT NULL,
    training_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_date ON predictions(prediction_date);
CREATE INDEX idx_diseases_name ON diseases(disease_name);
CREATE INDEX idx_diseases_crop ON diseases(crop_type);
