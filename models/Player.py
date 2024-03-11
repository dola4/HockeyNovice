from database.mongoDB import connection
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from pymongo import ReturnDocument

import secrets
from datetime import datetime

from .Invitation import Invitation
from .StatsGoaler import StatsGoaler
from .StatsPlayer import StatsPlayer


db = connection()

class Player:
    def __init__(self, team_id, email, password, first_name, last_name, niveau, number, phone, position, photo_url, _id=None):
        self.team_id = team_id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.niveau = niveau
        self.number = number
        self.phone = phone
        self.position = position
        self.photo_url = photo_url
        self.stats_player = StatsPlayer()
        self.stats_goaler = StatsGoaler()
        self._id = _id
    
    def to_dict(self):
        return {
            "_id": self._id if isinstance(self._id, ObjectId) else str(self._id),
            "team_id": self.team_id if isinstance(self.team_id, ObjectId) else ObjectId(self.team_id),        
            "email": self.email,
            "password": self.password,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "niveau": self.niveau,
            "number": self.number,
            "phone": self.phone,
            "position": self.position,
            "photo_url": self.photo_url,
            "stats_player": self.stats_player.__dict__ if self.stats_player else None,
            "stats_goaler": self.stats_goaler.__dict__ if self.stats_goaler else None,
        }
    
    def to_session_dict(self):
        session_dict = self.to_dict()
        session_dict['_id'] = str(session_dict['_id']) if session_dict['_id'] else None
        session_dict['team_id'] = str(session_dict['team_id']) if session_dict['team_id'] else None
        return session_dict
    
    def from_dict(self, player_dict):
        self._id = player_dict["_id"]
        self.team_id = player_dict["team_id"]
        self.email = player_dict["email"]
        self.password = player_dict["password"]
        self.first_name = player_dict["first_name"]
        self.last_name = player_dict["last_name"]
        self.niveau = player_dict["niveau"]
        self.number = player_dict["number"]
        self.phone = player_dict["phone"]
        self.position = player_dict["position"]
        self.photo_url = player_dict["photo_url"]
        self.stats_player = StatsPlayer().from_dict(player_dict["stats_player"])
        self.stats_goaler = StatsGoaler().from_dict(player_dict["stats_goaler"])
        return self
    
    
    
    def create(self):
        try:
            token = secrets.token_urlsafe(16)
            initial_password = self.password
            hashed_password = generate_password_hash(initial_password)
            self.password = hashed_password

            player_dict = self.to_dict()
            player_dict.pop("_id", None)

            inserted_player = db.players.insert_one(player_dict)
            self._id = inserted_player.inserted_id

            today = datetime.now()

            invitation = Invitation(self._id, token, today, "envoye")
            print(f"invitation: {invitation.to_dict()}")
            if invitation.create():
                invitation.send_by_sms(self.phone, self.email, initial_password, token)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False


    
    @classmethod
    def find_one(cls, player_id):
        try:
            player_data = db.players.find_one({"_id": ObjectId(player_id)})
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], niveau=player_data['niveau'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player = StatsPlayer.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler = StatsGoaler.from_dict(player_data.get("stats_goaler", {}))
                print(f'class method player_name: {player.first_name} player_stats: {player.stats_player.to_dict()} goaler_stats: {player.stats_goaler.to_dict()}')
                return player
            else:
                return "Player not found"
        except Exception as e:
            print(e)
            return None
        
    def find_players_by_team(team_id):
        try:
            players = []
            cursor = db.players.find({"team_id": ObjectId(team_id)})
            for player_data in cursor:
                player = Player(
                    _id=str(player_data['_id']), 
                    team_id=player_data['team_id'], 
                    email=player_data['email'], 
                    password=player_data['password'], 
                    first_name=player_data['first_name'], 
                    last_name=player_data['last_name'],
                    niveau=player_data['niveau'], 
                    number=player_data['number'], 
                    phone=player_data['phone'], 
                    position=player_data['position'], 
                    photo_url=player_data['photo_url'])
                
                player.stats_player = StatsPlayer.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler = StatsGoaler.from_dict(player_data.get("stats_goaler", {}))
                players.append(player)
            
            if len(players) == 0:
                return []
            
            return players
        except Exception as e:
            print(e)
            return []

    @classmethod
    def find_one_by_email(cls, email):
        try:
            player_data = db.players.find_one({"email": email})
            print(f"player_data : {player_data}")
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], niveau=player_data['niveau'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                return player
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def find_one_by_number(cls, number):
        try:
            player_data = db.players.find_one({"number": number})
            if player_data:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], niveau=player_data['niveau'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                return player
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    @classmethod
    def find_all(cls):
        try:
            players = []
            cursor = db.players.find()
            print(cursor)
            for player_data in cursor:
                player = cls(_id=str(player_data['_id']), team_id=player_data['team_id'], email=player_data['email'], password=player_data['password'], first_name=player_data['first_name'], last_name=player_data['last_name'], niveau=player_data['niveau'], number=player_data['number'], phone=player_data['phone'], position=player_data['position'], photo_url=player_data['photo_url'])
                player.stats_player.from_dict(player_data.get("stats_player", {}))
                player.stats_goaler.from_dict(player_data.get("stats_goaler", {}))
                players.append(player)
            
            if len(players) == 0:
                return "No players found"
            
            return players
        except Exception as e:
            print(e)
            return None

    def update(self):
        try:
            db.players.update_one({"_id": ObjectId(self._id)}, {"$set": {
                "team_id": self.team_id, 
                "email": self.email, 
                "password": self.password, 
                "first_name": self.first_name, 
                "last_name": self.last_name, 
                "niveau": self.niveau, 
                "number": self.number, 
                "phone": self.phone, 
                "position": self.position, 
                "photo_url": self.photo_url,
            }})
            return True
        except Exception as e:
            print(e)
            return False
    
    def delete(self):
        try:
            db.players.delete_one({"_id": ObjectId(self._id)})
            return True
        except Exception as e:
            print(e)
            return False
    
    def increment_player_stat(self, stat_type):
        self.stats_player.increment_stat(stat_type)
    
    def decrement_player_stat(self, stat_type):
        self.stats_player.decrement_stat(stat_type)

    def increment_goaler_stat(self, stat_type):
        self.stats_goaler.increment_stat(stat_type)
    
    def decrement_goaler_stat(self, stat_type):
        self.stats_goaler.decrement_stat(stat_type)
    
    def update_player_stats(self, operation, stat_type):
        try:
            if operation == "increment_player":
                self.increment_player_stat(stat_type)
            elif operation == "decrement_player":
                self.decrement_player_stat(stat_type)
            elif operation == "increment_goaler":
                self.increment_goaler_stat(stat_type)
            elif operation == "decrement_goaler":
                self.decrement_goaler_stat(stat_type)
            
            if operation == "increment_player" or operation == "decrement_player":
                if self._id:
                    updated_stats = {"stats_player": self.stats_player.to_dict()}
                    db.players.update_one({"_id": ObjectId(self._id)}, {"$set": updated_stats})
                    return True
                else:
                    return "Player not found"
            elif operation == "increment_goaler" or operation == "decrement_goaler":
                if self._id:
                    updated_stats = {"stats_goaler": self.stats_goaler.to_dict()}
                    db.players.update_one({"_id": ObjectId(self._id)}, {"$set": updated_stats})
                    return True
                else:
                    return "Player not found"
        except Exception as e:
            print(e)
            return False
        

    

        

        