# TODO App

A web application to manage tasks, built with **Flask**, **PostgreSQL**, and **MongoDB**, featuring authentication via **Google OAuth**.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
    ```

2. Run te application
   `python run.py`

3. Make sure the app runs on `http://localhost:5000` for the OAuth services to function correctly.

---

## Configuration

* Fill the .env file with the required values:
   ```plaintext
   FLASK_SECRET_KEY=<your_flask_secret_key>
   SECRET_KEY=<your_secret_key>
   GOOGLE_CLIENT_ID=<your_google_client_id>
   GOOGLE_CLIENT_SECRET=<your_google_client_secret>
   GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
   GOOGLE_API_SCOPE="openid profile email"
   POSTGRES_URI=<your_postgresql_uri>
   MONGO_URI=<your_mongodb_uri>
    ```

* An example file .env.example is included in the repository

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

---

## Notes

* **PostgreSQL** is used for user data.
* **MongoDB** is used for managing tasks (CRUD operations)
