import os
from app import create_app
from app.extensions import socketio
from app.services.seeder import seed_admin, seed_test_user

app = create_app()

if __name__ == "__main__":
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        with app.app_context():
            seed_admin()
            seed_test_user()

    flask_debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    socketio.run(app, debug=flask_debug, host="[IP_ADDRESS]", port=5000, allow_unsafe_werkzeug=True)
