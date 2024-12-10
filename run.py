from dotenv import load_dotenv
load_dotenv()  # Cargar variables de entorno desde .env
from app import app
import os

print(f"App initialized with secret key: {app.secret_key}")
print(f"Loaded FLASK_SECRET_KEY: {os.getenv('FLASK_SECRET_KEY')}")


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
