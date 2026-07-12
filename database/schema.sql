-- ==========================================
-- AI Customer Support Chatbot Database
-- ==========================================

-- Create Database
CREATE DATABASE IF NOT EXISTS ai_customer_support;

-- Use Database
USE ai_customer_support;

-- ==========================================
-- Customers Table (Updated with Role)
-- ==========================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Bcrypt hash yahan save hoga
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- Chat History Table
-- ==========================================

CREATE TABLE IF NOT EXISTS chat_history (
    chat_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    chat_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_chat
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
    ON DELETE CASCADE
);

-- ==========================================
-- Complaints Table (Updated Status to ENUM)
-- ==========================================

CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    complaint TEXT NOT NULL,
    status ENUM('Pending', 'In Progress', 'Resolved') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer_complaint
    FOREIGN KEY(customer_id)
    REFERENCES customers(customer_id)
    ON DELETE CASCADE
);

-- ==========================================
-- Sample Customers (With Bcrypt Hashed Passwords)
-- ==========================================

-- Note: In sabka temporary plain-text password 'password123' hai 
-- jise bcrypt se hash kiya gaya hai ($2b$12$...)
INSERT INTO customers(name, email, password, role)
VALUES
('System Admin', 'admin@gmail.com', '$2b$12$EixZaYVK1fsby1Z7ftM7eOzKqU.5MhY3sJkX3C4O7Qe7Rz6CqYmO.', 'admin'),
('Pooja', 'pooja@gmail.com', '$2b$12$EixZaYVK1fsby1Z7ftM7eOzKqU.5MhY3sJkX3C4O7Qe7Rz6CqYmO.', 'user'),
('Rahul', 'rahul@gmail.com', '$2b$12$EixZaYVK1fsby1Z7ftM7eOzKqU.5MhY3sJkX3C4O7Qe7Rz6CqYmO.', 'user'),
('Aman', 'aman@gmail.com', '$2b$12$EixZaYVK1fsby1Z7ftM7eOzKqU.5MhY3sJkX3C4O7Qe7Rz6CqYmO.', 'user')
ON DUPLICATE KEY UPDATE role=VALUES(role);

-- ==========================================
-- Sample Chat History
-- ==========================================

INSERT INTO chat_history(customer_id, question, answer)
VALUES
(2, 'What is your refund policy?', 'You can request a refund within 7 days.'),
(3, 'How can I track my order?', 'Please provide your order ID.');

-- ==========================================
-- Sample Complaints
-- ==========================================

INSERT INTO complaints(customer_id, complaint, status)
VALUES
(2, 'Received damaged product', 'Pending'),
(3, 'Order not delivered', 'Resolved');

-- ==========================================
-- Verify Data
-- ==========================================

SELECT * FROM customers;
SELECT * FROM chat_history;
SELECT * FROM complaints;