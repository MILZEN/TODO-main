# Troubleshooting

## Common Issues

### 1. **Error: "MONGO_URI must be set"**
   - Ensure the `MONGO_URI` value in `.env` is correct and points to a valid MongoDB instance.

### 2. **OAuth Callback URL not working**
   - Check that the `redirect_uri` in Google Cloud Console matches `http://localhost:5000/auth/callback`.

### 3. **Environment variables not loading**
   - Verify that the `.env` file exists in the root of the project and contains valid values.

### 4. **Deployment issues on Render**
   - Confirm that all required environment variables are set in the Render dashboard.
   - Ensure the app is installed with the correct dependencies (`pip install -r requirements.txt`).

---
