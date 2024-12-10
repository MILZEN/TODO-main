# Authentication API

## Overview
This application uses **Google OAuth** for user authentication. Google OAuth allows users to log in securely using their Google account, providing a seamless authentication flow.

## Login with Google OAuth

Users can authenticate by logging in with their Google account.

### Authentication Flow

1. **User clicks the 'Login with Google' button**.
2. **Redirect to Google OAuth**: The user is redirected to Google's OAuth 2.0 server.
3. **User grants permissions**: After granting necessary permissions, Google redirects the user back to the application.
4. **Access Token**: The application retrieves an access token from Google to authenticate the user.
5. **Session creation**: A session is created to keep the user logged in.

### Request

No manual API request is required from the user side. The authentication flow is handled via a redirection to Google and a callback handler in the app.

### Response

- **Success**: The user is logged in, and a session is created.
- **Failure**: If authentication fails, the user is redirected back to the login page with an error message.

### Example

- **Login URL**: `/login/google`
- **Redirect URL after successful login**: `/home/<username>`

For any error, the user is redirected back to the login page with an error message.

## Logout

At the moment, to log out, users need to click on any button in the navbar (Login or Sign in).
