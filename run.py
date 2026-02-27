from crucible_ui import app
from crucible_ui.routes import sync_workspace_headers

if __name__ == "__main__":
    print("--- CRUCIBLE TURBINE: UI SYSTEM ONLINE ---")
    with app.app_context():
        sync_workspace_headers()
    print("[PORT] http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
