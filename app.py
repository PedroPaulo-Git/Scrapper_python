from flask import Flask
from routes.userbasicinfos import user_basic_infos_route
from routes.followers import followers_route
from routes.highlight import highlights_route
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # permite todas as origens (inclusive localhost:3000)

# Registrando a rota
app.register_blueprint(highlights_route)
app.register_blueprint(user_basic_infos_route)
app.register_blueprint(followers_route)

if __name__ == "__main__":
    app.run(debug=True)
