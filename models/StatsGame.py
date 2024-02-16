from bson.objectid import ObjectId


from database.mongoDB import connection
from .singlePlayerStats import singleStatsPlayer
from .singleGoalerStats import singleStatsGoaler
from .StatsTeam import StatsTeam
from .Player import Player
from .Game import Game



db = connection()

class StatsGame:
    def __init__(self, player_id, game_id, _id = None):
        self._id = _id
        self.player_id = player_id
        self.game_id = game_id
        self.stats_game_player = singleStatsPlayer()
        self.stats_game_goaler = singleStatsGoaler()
        
        
    def to_dict(self):
        data = {
            'player_id': self.player_id,
            'game_id': self.game_id,
            'stats_game_player': self.stats_game_player.__dict__ if self.stats_game_player else singleStatsPlayer().to_dict(),
            'stats_game_goaler': self.stats_game_goaler.__dict__ if self.stats_game_goaler else singleStatsGoaler().to_dict(),
        }
        if self._id:
            data["_id"] = self._id if isinstance(self._id, ObjectId) else str(self._id)
        return data

        
    def from_dict(self, stats_game_dict):
        self._id = stats_game_dict["_id"]
        self.player_id = stats_game_dict.get('player_id')
        self.game_id = stats_game_dict.get('game_id')

        self.stats_game_player = singleStatsPlayer().from_dict(stats_game_dict['stats_game_player'])
        self.stats_game_goaler = singleStatsGoaler().from_dict(stats_game_dict['stats_game_goaler'])
        return self
    
    def save(self):
        if self._id is None:
            result = db.statsGame.insert_one(self.to_dict())
            self._id = result.inserted_id
            return True
        else:
            result = db.statsGame.update_one({'_id': ObjectId(self._id)}, {'$set': self.to_dict()})
            return result.modified_count > 0
        

    def update_team_stats(self):  
        team = Game.find_team_game(self.game_id)
        team_stat = team.stats_team
        player = Player.find_one(self.player_id)
        player_stat = player.stats_player
    
        # Mise à jour des statistiques de l'équipe en fonction du score
        if self.team_score > self.opponent_score:
            team_stat.increment_stat("victory")
        elif self.team_score < self.opponent_score:
            team_stat.increment_stat("defeat")
        else:  # self.team_score == self.opponent_score
            team_stat.increment_stat("defeat_in_OT")
    
        # Sauvegarde des modifications des statistiques de l'équipe
        team.save()  # Assurez-vous que cette méthode existe dans la classe de l'équipe

        

    @classmethod
    def find_or_create(cls, player_id, game_id):
        stats_game = db.statsGame.find_one({'player_id': player_id, 'game_id': game_id})
        if stats_game:
            # Crée une instance avec les bons arguments
            return cls(player_id=player_id, game_id=game_id).from_dict(stats_game)
        else:   
            # Crée une nouvelle instance sans définir _id
            return cls(player_id=player_id, game_id=game_id)







    def update_stat(self, is_goaler, operation, stat_type):
        # Sélectionne l'objet de statistiques approprié (global ou spécifique au match)
        stat_object = self.stats_game_goaler if is_goaler else self.stats_game_player

        # Mise à jour de la statistique spécifique pour le match
        if operation == "increment":
            stat_object.increment_stat(stat_type)
        elif operation == "decrement":
            stat_object.decrement_stat(stat_type)

        # Sauvegarde les changements dans la base de données
        self.save()



        
    def delete(self):
        if self._id is not None:
            db.statsGame.delete_one({'_id': ObjectId(self._id)})
            return True
        return False
    
    