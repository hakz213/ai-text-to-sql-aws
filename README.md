# AI Text-to-SQL (AWS)

## Overview
This project converts natural language questions into SQL queries using Amazon Bedrock, executes them on Aurora PostgreSQL via AWS Lambda, and returns real data.

## Architecture
User → Lambda → Bedrock → SQL → Aurora → Result

## Technologies
- AWS Lambda
- Amazon Bedrock (Claude Haiku)
- Aurora PostgreSQL
- pg8000
- VPC + Endpoints
