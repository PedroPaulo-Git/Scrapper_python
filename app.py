from flask import Flask, request, redirect
from routes.userbasicinfos import user_basic_infos_route
from routes.followers import followers_route
from routes.highlight import highlights_route
from routes.user_cache import user_info_cache  # <- ADICIONA ISSO

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://instaviewpro.vercel.app","http://localhost:3000"]) # permite todas as origens (inclusive localhost:3000)

# Registrando a rota
app.register_blueprint(highlights_route)
app.register_blueprint(user_basic_infos_route)
app.register_blueprint(followers_route)
app.register_blueprint(user_info_cache) 

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form
    if data.get('purchase') == 'true':
        # Aqui você pode salvar as informações da compra
        return redirect('/upssel')
    return '', 200

if __name__ == "__main__":
    app.run(debug=True)
