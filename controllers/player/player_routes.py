from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import os
import shutil

from models.Invitation import Invitation
from models.Admin import Admin
from models.Player import Player
from models.Team import Team

player_routes = Blueprint('player_routes', __name__)


@player_routes.route("/player_profil/<string:player_id>", methods=['GET'])
def player_profil(player_id):
    if 'player' in session:
        player_session = session['player']
        player = Player.find_one(player_id)
        team = Team.find_one(player.team_id)
        
        return render_template('client/player_profil.html', player=player, team=team)
    else:
        return redirect(url_for('common_routes.login'))
    
    

@player_routes.route("/edit_info/<string:player_id>", methods=['GET', 'POST'])
def edit_info(player_id):
    if 'player' in session:
        player = Player.find_one(player_id)
        if request.method == 'POST':
            player.first_name = request.form['firstName']
            player.last_name = request.form['lastName']
            player.email = request.form['email']
            player.phone = request.form['phone']
            
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
            return redirect(url_for('common_routes.player_info', player_id=player_id))
                
            
        
        return render_template('client/edit_info.html', player=player)
    else:
        return redirect(url_for('common_routes.login'))
    
@player_routes.route("/change_password/<string:player_id>", methods=['GET', 'POST'])
def change_password(player_id):
    if 'player' in session:
        player = Player.find_one(player_id)
        if request.method == 'POST':
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            
            if check_password_hash(player.password, old_password):
                if new_password == confirm_password:
                    hashed_password = generate_password_hash(new_password)
                    player.password = hashed_password
                    player.update()

                    # Mise à jour de la session avec la version sérialisable
                    session['player'] = player.to_session_dict()

                    return redirect(url_for('player_routes.player_profil', player_id=player_id))
                else:
                    return render_template('client/change_password.html', player=player, error="Passwords do not match")
        
        return render_template('client/change_password.html', player=player)
    else:
        return redirect(url_for('common_routes.login'))
    
    
@player_routes.route("/confirm_invitation/<string:player_id>", methods=['GET', 'POST'])    
def confirm_invitation(player_id):
    invitation = Invitation.find_one_by_player(player_id)
    if request.method == 'POST':
        token = request.form['token']
        initial_password = request.form['initial_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']
        
        if token == invitation.token:
            if new_password == confirm_new_password and new_password != initial_password:
                hashed_password = generate_password_hash(new_password)
                player = Player.find_one(player_id)
                player.password = hashed_password
                player.update()
                
                invitation.status = "accepte"
                invitation.update()
                
                session['player'] = player.to_session_dict()
                return redirect(url_for('player_routes.player_profil', player_id=player_id))

    else:
        return render_template('client/confirm_invitation.html', invitation=invitation, player_id=player_id)
                
    
@player_routes.route("/contact_admin/", methods=['GET'])
def contact_admin():
    return render_template('common/contact_admin.html')