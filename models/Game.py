from bson.objectid import ObjectId, InvalidId


from database.mongoDB import connection
from .Team import Team

from .Player import Player


db = connection()




class Game:
    def __init__(self, team_id=None, opponent=None, date=None, time=None, _id=None, team_score=0, opponent_score=0):
        self._id = _id
        self.team_id = team_id
        self.opponent = opponent
        self.date = date
        self.time = time
        self.team_score = team_score
        self.opponent_score = opponent_score


        

    def to_dict(self):
        return {
            'team_id': self.team_id,
            'opponent': self.opponent,
            'date': self.date,
            'time': self.time,
            'team_score': self.team_score,
            'opponent_score': self.opponent_score,
        }
        
        
    def from_dict(self, game_dict):
        self._id = game_dict.get('_id')
        self.team_id = game_dict.get('team_id')
        self.opponent = game_dict.get('opponent')
        self.date = game_dict.get('date')
        self.time = game_dict.get('time')
        self.team_score = game_dict.get('team_score', 0)
        self.opponent_score = game_dict.get('opponent_score', 0)
        return self

    
        
    def save(self):
        if self._id is None:
            result = db.games.insert_one(self.to_dict())
            self._id = result.inserted_id
            return True
        else:
            result = db.games.update_one({'_id': ObjectId(self._id)}, {'$set': self.to_dict()})
            return result.modified_count > 0
        
    
    @classmethod
    def find_game(cls, game_id):
        try:
            _id = ObjectId(game_id)
            game_data = db.games.find_one({'_id': _id})
            if game_data:
                return cls().from_dict(game_data)  
            else:
                return None
        except InvalidId:
            return None


        
    def find_team(self):
        team = Team.find_one(self.team_id)
        return team
    
    @classmethod
    def find_all_games_for_team(cls, team_id):
        games_data = db.games.find({'team_id': team_id})
        games = []
        for game_data in games_data:
            game = cls(
                team_id=game_data['team_id'],
                opponent=game_data['opponent'],
                date=game_data['date'],
                time=game_data['time'],
                _id=game_data['_id']
            )
            games.append(game)
        return games



    @classmethod
    def find_stats_for_game(cls, game_id):
        
        from .StatsGame import StatsGame
        
        stats_game_data = db.statsGame.find({'game_id': game_id})
        stats_for_game = []
        for stats_game_dict in stats_game_data:
            stats_game = StatsGame().from_dict(stats_game_dict)
            player = Player.find_one(stats_game.player_id)
            stats_for_game.append({
                "player": player,
                "stats": stats_game
            })
        return stats_for_game
    
    def delete(self):
        if self._id is not None:
            db.games.delete_one({'_id': ObjectId(self._id)})
            return True
        return False
    

            
    

    

            