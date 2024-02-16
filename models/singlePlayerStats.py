from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId

db = connection()

class singleStatsPlayer:
    def __init__(self, goals=0, assists=0, shots=0, faceoff_played=0, 
                 faceoff_win=0, turnovers=0, penalty_minutes=0, time_on_ice=0, 
                 blocked_shots=0, plus_minus=0):

        self.goals = goals
        self.assists = assists
        self.shots = shots
        self.faceoff_played = faceoff_played
        self.faceoff_win = faceoff_win
        self.turnovers = turnovers
        self.penalty_minutes = penalty_minutes
        self.time_on_ice = time_on_ice
        self.blocked_shots = blocked_shots
        self.plus_minus = plus_minus
    
    
    @property
    def points(self):
        return self.goals + self.assists

    def to_dict(self):
        return {
            'goals': self.goals,
            'assists': self.assists,
            'shots': self.shots,
            'faceoff_played': self.faceoff_played,
            'faceoff_win': self.faceoff_win,
            'turnovers': self.turnovers,
            'penalty_minutes': self.penalty_minutes,
            'time_on_ice': self.time_on_ice,
            'blocked_shots': self.blocked_shots,
            'plus_minus': self.plus_minus,
            'points': self.points,
        }

    
    @classmethod
    def from_dict(cls, data):
        if data is None:
            return cls()  # Retourne une instance par défaut si aucune donnée
        # Initialisez l'instance avec des données spécifiques
        return cls(
            goals=data.get('goals', 0),
            assists=data.get('assists', 0),
            shots=data.get('shots', 0),
            faceoff_played=data.get('faceoff_played', 0),
            faceoff_win=data.get('faceoff_win', 0),
            turnovers=data.get('turnovers', 0),
            penalty_minutes=data.get('penalty_minutes', 0),
            time_on_ice=data.get('time_on_ice', 0),
            blocked_shots=data.get('blocked_shots', 0),
            plus_minus=data.get('plus_minus', 0)
        )

    
    def increment_stat(self, stat_type):
        if hasattr(self, stat_type):
            setattr(self, stat_type, getattr(self, stat_type) + 1)
        else:
            print("Stat type not found")

    def decrement_stat(self, stat_type):
        if hasattr(self, stat_type):
            current_value = getattr(self, stat_type)
        
            if stat_type == "plus_minus":
                setattr(self, stat_type, current_value - 1)

            elif current_value > 0:  
                setattr(self, stat_type, current_value - 1)
                
            else:
                print(f"Cannot decrement {stat_type}, already at zero.")
        else:
            print("Stat type not found")



