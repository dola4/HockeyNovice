from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId

from models.Invitation import Invitation
from models.Admin import Admin
from models.Player import Player
from models.Team import Team

common_routes = Blueprint('common_routes', __name__)


@common_routes.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        player = Player.find_one_by_email(email)
        print(player)
        admin = Admin.find_one_by_email(email)
        

        if player:
            print("Player:", player)
            if check_password_hash(player.password, password):
                session['player'] = player.to_session_dict()
                invitation = Invitation.find_one_by_player(player._id)
                if invitation:
                    if invitation.status == "envoye":
                        return redirect(url_for('player_routes.confirm_invitation', player_id=player._id))
                
                    elif invitation.status == "accepte":
                        return redirect(url_for('player_routes.player_profil', player_id=player._id))
                
                    else:
                        return redirect(url_for('player_routes.contact_admin'))
                else:
                    return redirect(url_for('player_routes.contact_admin'))
            else:
                return render_template('common/login.html', error="Invalid password")
            
        elif admin:    
            if check_password_hash(admin.password, password):
                session['admin'] = admin.to_dict()
                return redirect(url_for('admin_routes.admin_dashboard'))
            
            else:
                return render_template('common/login.html', error="Invalid password")
        else:
            return render_template('common/login.html', error="Invalid email")


    return render_template('common/login.html')


@common_routes.route('/all_teams', methods=['GET'])
def all_teams():
    if 'admin' not in session and 'player' not in session:
        return redirect(url_for('common_routes.login'))

    player_id = session['player']['_id'] if 'player' in session else None
    teams = Team.find_all()
    for team in teams:
        team.fetch_players()

    return render_template('common/all_teams.html', teams=teams, player_id=player_id)


@common_routes.route('/team_info/<team_id>', methods=['GET'])
def team_info(team_id):
    if 'admin' not in session and 'player' not in session:
        return redirect(url_for('common_routes.login'))

    team = Team.find_one(team_id)
    players = Player.find_players_by_team(team_id)
    player_id = session['player']['_id'] if 'player' in session else None

    return render_template('common/team_info.html', team=team, players=players, player_id=player_id)

@common_routes.route('/player_info/<player_id>', methods=['GET'])
def player_info(player_id):
    if 'admin' not in session and 'player' not in session:
        return redirect(url_for('common_routes.login'))

    player = Player.find_one(player_id)
    team = Team.find_one(player.team_id)
    player_id = session['player']['_id'] if 'player' in session else None

    return render_template('common/player_info.html', player=player, team=team, player_id=player_id)


@common_routes.route('/deconnect', methods=['GET'])
def deconnect():
    session.clear()
    return redirect(url_for('common_routes.login'))