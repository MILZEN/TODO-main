# Configuration Guide

---

## Google OAuth Setup

To set up Google OAuth credentials:
   1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
   2. Create a new project or select an existing one.
   3. Navigate to **APIS & Services** > **Library**.
   4. Search for **Google People API** and enable it.
   5. Click Create Credentials and select OAuth 2.0 Client IDs.
   6. Configure the consent screen and add `http://localhost:5000` (for development) and your deployed app URL as authorized redirect URIs.
   7. Save the credentials and copy the Client ID and Client Secret into your .env file.

Refer to the [official Google documentation](https://developers.google.com/people/?hl=es_419) for more details.

## Configuring Databases
1. **PostgreSQL**:
   - Create a PostgreSQL database for user authentication.
   - Add your host, user, password, and database name to `.env`.
2. **MongoDB**:
   - Set up a MongoDB database for task management.
   - Use a connection string (e.g., `mongodb+srv://<username>:<password>@cluster.mongodb.net/myFirstDatabase`) and set it as `MONGO_URI` in `.env`.