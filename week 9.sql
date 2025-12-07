CREATE DATABASE IF NOT EXISTS week9_db;
USE week9_db;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS incidents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    incident_id VARCHAR(50) UNIQUE,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    severity VARCHAR(50),
    status VARCHAR(50),
    assigned_to VARCHAR(50),
    resolution_time_hours FLOAT,
    description TEXT,
    date DATE
);


INSERT INTO users (username, password_hash)
VALUES ('admin', SHA2('admin123',256));

INSERT INTO incidents (incident_id, category, subcategory, severity, status, assigned_to, resolution_time_hours, description, date)
VALUES
('INC-001','Malware','Ransomware','High','Open','John',5.0,'Malware detected','2025-01-01');


