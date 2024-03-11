from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId

db = connection()

# Classe Stats pour les goalers et les matchs

class singleStatsGoaler:
    def __init__(self, save=0, goals_given=0, time_on_ice=0, goals=0, assists=0, penalty_minutes=0):
        self.save = save
        self.goals_given = goals_given
        self.time_on_ice = time_on_ice
        self.goals = goals
        self.assists = assists
        self.penalty_minutes = penalty_minutes

    @property
    def points(self):
        return self.goals + self.assists

    @property
    def shots_against(self):
        return self.save + self.goals_given
    
    

    def to_dict(self):
        return {
            'save': self.save,
            'goals_given': self.goals_given,
            'time_on_ice': self.time_on_ice,
            'goals': self.goals,
            'assists': self.assists,
            'penalty_minutes': self.penalty_minutes,
            'points': self.points,
            'shots_against': self.shots_against
        }
    
    @classmethod
    def from_dict(cls, data):
        save=data.get('save', 0),
        goals_given=data.get('goals_given', 0),
        time_on_ice=data.get('time_on_ice', 0),
        goals=data.get('goals', 0),
        assists=data.get('assists', 0),
        penalty_minutes=data.get('penalty_minutes', 0)
        return cls(
            save = save,
            goals_given = goals_given,
            time_on_ice = time_on_ice,
            goals = goals,
            assists = assists,
            penalty_minutes = penalty_minutes
        )
            

    def increment_stat(self, stat_type):
        if hasattr(self, stat_type):
            setattr(self, stat_type, getattr(self, stat_type) + 1)
        else:
            print("Stat type not found")
    
    def decrement_stat(self, stat_type):
        if hasattr(self, stat_type):
            current_value = getattr(self, stat_type)
            if current_value > 0:  
                setattr(self, stat_type, current_value - 1)
            else:
                print(f"Cannot decrement {stat_type}, already at zero.")
        else:
            print("Stat type not found")

        