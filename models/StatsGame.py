from bson.objectid import ObjectId


from database.mongoDB import connection
from .StatsPlayer import StatsPlayer
from .StatsGoaler  import StatsGoaler

from .Player import Player


db = connection()

class StatsGame:
    def __init__(self, player_id, game_id, team_score, opponent_score, _id = None):
        self._id = _id
        self.player_id = player_id
        self.game_id = game_id
        self.team_score = team_score
        self.opponent_score = opponent_score
        self.stats_game_player = StatsPlayer()
        self.stats_game_goaler = StatsGoaler()
        
        
    def to_dict(self):
        data = {
            'player_id': self.player_id,
            'game_id': self.game_id,
            'team_score': self.team_score,
            'opponent_score': self.opponent_score,
            'stats_game_player': self.stats_game_player.to_dict(),
            'stats_game_goaler': self.stats_game_goaler.to_dict()
        }
        if self._id:
            data["_id"] = self._id if isinstance(self._id, ObjectId) else str(self._id)
        return data

        
    def from_dict(self, stats_game_dict):
        self._id = stats_game_dict["_id"]
        self.player_id = stats_game_dict.get('player_id')
        self.game_id = stats_game_dict.get('game_id')
        self.team_score = stats_game_dict.get('team_score')
        self.opponent_score = stats_game_dict.get('opponent_score')
        self.stats_game_player = StatsPlayer().from_dict(stats_game_dict.get('stats_game_player'))
        self.stats_game_goaler = StatsGoaler().from_dict(stats_game_dict.get('stats_game_goaler'))
        return self
    
    def save(self):
        if self._id is None:
            result = db.stats_game.insert_one(self.to_dict())
            self._id = result.inserted_id
            return True
        else:
            result = db.stats_game.update_one({'_id': ObjectId(self._id)}, {'$set': self.to_dict()})
            return result.modified_count > 0
        
    def update_team_stats(self):
        from .Game import Game
        
        team = Game.find_team_game(self.game_id)
        team_stat = team.stats_team
        player = Player.find_one(self.player_id)
        player_stat = player.stats_player
        
        if self.team_score > self.opponent_score:
            team_stat.increment_stat("victory")
        if self.team_score < self.opponent_score:
            team_stat.increment_stat("defeat")
        if self.team_score == self.opponent_score:
            team_stat.increment_stat("defeat_in_OT")
        

    @classmethod
    def find_or_create(cls, player_id, game_id):
        stats_game = db.stats_game.find_one({'player_id': player_id, 'game_id': game_id})
        if stats_game:
            return cls().from_dict(stats_game)
        else:
            # Crée une nouvelle instance sans définir _id
            return cls(player_id, game_id, 0, 0)




    def update_stat(self, is_goaler, operation, stat_type):
        # Choisir l'objet de statistiques approprié en fonction du type de joueur
        stat_object = self.stats_game_goaler if is_goaler else self.stats_game_player

        # Mise à jour de la statistique
        current_value = getattr(stat_object, stat_type, 0)
        if operation == "increment":
            setattr(stat_object, stat_type, current_value + 1)
        elif operation == "decrement" and current_value > 0:
            setattr(stat_object, stat_type, current_value - 1)
        else:
            print("Operation not valid or stat is already at minimum")

        # Enregistrer les modifications
        self.save()

        
    def delete(self):
        if self._id is not None:
            db.stats_game.delete_one({'_id': ObjectId(self._id)})
            return True
        return False
    
    