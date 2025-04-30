from flask import Flask
from routes.userbasicinfos import userbasicinfos_bp
from routes.picture import picture_bp
from routes.highlight import highlight_bp


app = Flask(__name__)

# Registrar os Blueprints
app.register_blueprint(picture_bp, url_prefix='/picture')
app.register_blueprint(highlight_bp, url_prefix='/highlight')
app.register_blueprint(userbasicinfos_bp, url_prefix='/userbasicinfos')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
