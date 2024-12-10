# Main code, page will be deployed from here

from dotenv import load_dotenv
from app import app
import os

load_dotenv()  # Load environment variables from .env

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
