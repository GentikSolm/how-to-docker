from waitress import serve
from app import create_app

app = create_app()
# Note, that by default waitress has no logger.
print("Starting prod!", flush=True)
serve(app, host="0.0.0.0", port=8080)
