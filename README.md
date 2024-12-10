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

## Notes

* **PostgreSQL** is used for user data.
* **MongoDB** is used for managing tasks (CRUD operations)

---

## Additional Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Atlas](https://www.mongodb.com/atlas/database)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)
