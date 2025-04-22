from flask import Flask
from scada_ui.routes.dashboard import dashboard_bp
from scada_ui.routes.logs import logs_bp
from scada_ui.routes.components import components_bp

def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(components_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
