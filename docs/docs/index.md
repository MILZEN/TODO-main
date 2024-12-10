# TASKED App Documentation
---
Welcome to the documentation for TASKED application. This is a task management system built with Flask, using PostgreSQL and MongoDB. It supports user authentication through Google OAuth.

## Features
---
- User authentication via Google OAuth
- Task management with CRUD operations (Create, Read, Update, Delete)
- MongoDB for task storage
- PostgreSQL for user data
- API for authentication
- Automated tests with pytest
- GitHub Actions for deployment and testing

## Quick Start
---

### Clone the repository
```bash
git clone https://github.com/MILZEN/TODO-main
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set up Environment Variables
Create a `.env` file in the root of the project or copy `.env.example` and fill in the required values.

Example:
```plaintext
FLASK_SECRET_KEY="your-secret-key"
MYSQL_HOST="localhost"
MYSQL_USER="your-mysql-user"
MYSQL_PASSWORD="your-mysql-password"
MYSQL_DATABASE="your-database-name"
MONGO_URI="your-mongodb-uri"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"
GOOGLE_DISCOVERY_URL="https://accounts.google.com/.well-known/openid-configuration"
```

### Run the application
```bash
python run.py
```

The application must run on `http://localhost:5000` for Google OAuth to work correctly.