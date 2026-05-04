# Setup Guide

## 1. Create Aurora PostgreSQL
- Engine: Aurora PostgreSQL
- Public access: Yes
- Port: 5432

## 2. Create table
CREATE TABLE customers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  country VARCHAR(50),
  revenue INT
);

## 3. Insert sample data
('John Ltd', 'UK', 50000)
('Anna Corp', 'Germany', 70000)
('BlueTech', 'France', 90000)

## 4. Create Lambda
- Runtime: Python 3.10
- Attach pg8000 layer
- Add environment variables

## 5. Configure VPC
- Same VPC as Aurora
- Add Bedrock VPC endpoint

## 6. Enable Bedrock model
- Claude Haiku
