import os

from app import create_app
config_name = os.getenv('FLASK_CONFIG')
flask_app = create_app(config_name)
#if __name__ == "__main__":
#    app.run_server(debug=True,host='0.0.0.0')
