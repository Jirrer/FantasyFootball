import os
from flask import Flask
from flask_cors import CORS
from backend.draft import bp as draft_bp

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])
app.register_blueprint(draft_bp)


if __name__ == "__main__":
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", "5001"))
    app.run(debug=True, host=host, port=port)