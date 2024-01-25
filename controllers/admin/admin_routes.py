from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from werkzeug.security import check_password_hash
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import shutil
from datetime import datetime


from models.Admin import Admin
from models.Team import Team
from models.Player import Player
from models.Game import Game
from models.StatsGame import StatsGame

admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route('/admin_dasboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'admin' in session:
        all_teams = Team.find_all()
        return render_template('admin/admin_dashboard.html', teams=all_teams)
    else:
        return redirect(url_for('common_routes.login'))
    

@admin_routes.route('/admin_team/<string:team_id>', methods=['GET', 'POST'])
def admin_team(team_id):
    if 'admin' in session:
        team = Team.find_one(team_id)
        players = Player.find_players_by_team(team_id)
        games = Game.find_all_games_for_team(team_id)
        return render_template('admin/admin_team.html', team=team, players=players, games=games)
    else:
        return redirect(url_for('common_routes.login'))




@admin_routes.route('/played_match/<string:game_id>', methods=['GET'])
def played_match(game_id):
    game = Game.find_game(game_id)
    if not game:
        return "Jeu non trouvé", 404

    players_stats = Game.find_stats_for_game(game_id)
    
    return render_template('admin/played_matches.html', game=game, players_stats=players_stats)



@admin_routes.route('/admin_player/<string:player_id>', methods=['GET', 'POST'])
def admin_player(player_id):
    if 'admin' in session:
        player = Player.find_one(player_id)
        team = Team.find_one(player.team_id)
        print(f"player image : /static/{player.photo_url}")
        return render_template('admin/admin_player.html', player=player, team=team)
    else:
        return redirect(url_for('common_routes.login'))    
      
      
@admin_routes.route('/gameOn/<string:team_id>', methods=['GET', 'POST'])
def gameOn(team_id):
    if 'admin' in session:
        team = Team.find_one(team_id)
        if request.method == 'POST':
            opponent = request.form['opponent']
            date = datetime.today().strftime('%Y-%m-%d')
            time = datetime.now().strftime('%H:%M:%S')

            game = Game(
                team_id=team_id,
                opponent=opponent,
                date=date,
                time=time
            )
            game.save()

            # Sélectionnez les joueurs pour le match
            selected_players_ids = request.form.getlist('onGame')
            players = [Player.find_one(player_id) for player_id in selected_players_ids]

            return render_template('admin/gameOn.html', team=team, players=players, game=game)
        else:
            players = Player.find_players_by_team(team_id)
            return render_template('admin/gameOn.html', team=team, players=players)
    else:
        return redirect(url_for('common_routes.login'))
        


    
@admin_routes.route('/update_player_stats', methods=['POST'])
def update_player_stats():
    player_id = request.form.get('playerId')
    game_id = request.form.get('gameId')
    operation = request.form.get('operation')
    stat_type = request.form.get('statType')
    is_goaler = request.form.get('isGoaler') == 'true'  # Convertit la chaîne en booléen

    player = Player.find_one(player_id)
    if player:
        # Mise à jour des statistiques du joueur
        player.update_player_stats(operation, stat_type)

        # Mise à jour ou création des statistiques du match
        stats_game = StatsGame.find_or_create(player_id, game_id)
        stats_game.update_stat(is_goaler, operation, stat_type)
        stats_game.save()

        return jsonify({"success": True})
    else:
        return jsonify({"error": "Player not found"}), 404






@admin_routes.route('/create_team', methods=['GET', 'POST'])
def create_team():
    if 'admin' in session:
        if request.method == 'POST':
            team_name = request.form.get('teamName')
            team = Team(name=team_name)
            print(team.name)
            team.create()
            return redirect(url_for('admin_routes.admin_dashboard'))
        else:
            return render_template('admin/create_team.html')
    else:
        return redirect(url_for('common_routes.login'))
    

@admin_routes.route('/edit_team/<string:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    if 'admin' not in session:
        return redirect(url_for('common_routes.login'))

    team = Team.find_one(team_id)
    if request.method == 'POST':
        team_name = request.form.get('teamName')
        team.name = team_name
        team.update(team_id)
        return redirect(url_for('admin_routes.admin_dashboard'))
    else:
        return render_template('admin/edit_team.html', team=team)

@admin_routes.route('/delete_team/<string:team_id>', methods=['POST'])
def delete_team(team_id):
    if 'admin' not in session:
        return redirect(url_for('common_routes.login'))

    Team.delete(team_id)
    return redirect(url_for('admin_routes.admin_dashboard'))


@admin_routes.route('/create_player/<string:team_id>', methods=['GET', 'POST'])
def create_player(team_id):
    if 'admin' in session:
        if request.method == 'POST':
            team_id = team_id
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            niveau = request.form.get('niveau')
            number = request.form.get('number')
            phone = request.form.get('phone')
            position = request.form.get('position')

            file = request.files['photo']
            if file:
                filename = secure_filename(file.filename)
                path = os.path.join('static/media/images_joueurs', filename)
                file.save(path)
                photo_url = url_for('static', filename='media/images_joueurs/' + filename)
            else:
                photo_url = None  

            new_player = Player(
                team_id=team_id,
                email=email,
                password= first_name + number,
                first_name=first_name,
                last_name=last_name,
                niveau=niveau,
                number=number,
                phone=phone,
                position=position,
                photo_url=photo_url
            )
            new_player.create()
            
            return redirect(url_for('admin_routes.admin_team', team_id=team_id))
        else:
            team = Team.find_one(team_id)
            return render_template('admin/create_player.html', team=team)
    else:
        return redirect(url_for('common_routes.login'))
    
    
@admin_routes.route('/edit_player/<string:player_id>', methods=['Get', 'POST'])
def edit_player(player_id):
    if 'admin' in session:
        player = Player.find_one(player_id)
        if request.method == 'POST':
            # Mettre à jour les informations du joueur
            player.first_name = request.form.get('firstName')
            player.last_name = request.form.get('lastName')
            player.niveau = request.form.get('niveau')
            player.number = request.form.get('number')
            player.position = request.form.get('position')
            
            file = request.files['photo']
            if file:
                
                old_photo_path = os.path.join('static/media/images_joueurs', os.path.basename(player.photo_url))
                if os.path.exists(old_photo_path):
                    new_old_photo_path = os.path.join('static/media/anciennes_images_joueurs', os.path.basename(player.photo_url))
                    shutil.move(old_photo_path, new_old_photo_path)
                    
                filename = secure_filename(file.filename)
                path = os.path.join('static/media/images_joueurs', filename)
                file.save(path)
                photo_url = url_for('static', filename='media/images_joueurs/' + filename)
                player.photo_url = photo_url
            player.update()
            return redirect(url_for('admin_routes.admin_team', team_id=player.team_id))
        else:
            team = Team.find_one(player.team_id)
            return render_template('admin/edit_player.html', player=player, team=team)
    else:
        return redirect(url_for('common_routes.login'))



@admin_routes.route('/delete_player/<string:player_id>', methods=['GET', 'POST'])
def delete_player(player_id):
    if 'admin' in session:
        player = Player.find_one(player_id)
        if player:
            player.delete()
            return redirect(url_for('admin_routes.admin_team', team_id=player.team_id))
        else:
            return "Joueur non trouvé", 404
    else:
        return redirect(url_for('common_routes.login'))

