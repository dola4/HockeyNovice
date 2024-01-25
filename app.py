from flask import Flask
from database.mongoDB import connection
from controllers.admin.admin_routes import admin_routes
from controllers.common.common_routes import common_routes
from controllers.player.player_routes import player_routes

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
db = connection()

app.register_blueprint(admin_routes)
app.register_blueprint(common_routes)
app.register_blueprint(player_routes)

if __name__ == '__main__':
    app.run(debug=True)
