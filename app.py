from flask import Flask
from routes.userbasicinfos import user_basic_infos_route
from routes.followers import followers_route


app = Flask(__name__)

# Registrando a rota
app.register_blueprint(user_basic_infos_route)
app.register_blueprint(followers_route)

if __name__ == "__main__":
    app.run(debug=True)
