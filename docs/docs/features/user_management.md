# User Management

This section covers the user authentication and management system in the application.

## Authentication
- **Google OAuth** is used to authenticate users.
- Users can also manually register by providing their email, username, password and their first and last name.

### User Registration
- With a successful manual registration, users are redirected to the login page to login with their email and password. 
- Upon successful registration via Google OAuth, users are redirected to their home page.
- All registered users are stored in a PostgreSQL database, with details like username, email, and authentication method.

### User Flow
1. The user registers or logs in using their Google account or manually with their email and password.
2. Upon successful login, a session is created, and the user is redirected to their home page where they can manage tasks.

## User Data
User information, including login credentials, is securely stored in a PostgreSQL database.
