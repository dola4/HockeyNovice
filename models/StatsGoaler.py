from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId

db = connection()

# Classe Stats pour les goalers et les matchs

class StatsGoaler:
    def __init__(self, games_played=0, wins=0, losses=0, save=0, goals_given=0, time_on_ice=0, goals=0, assists=0, penalty_minutes=0):
        self.games_played = games_played
        self.wins = wins
        self.losses = losses
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
    def shot_against(self):
        return self.goals_given + self.save
    
    @property
    def points_per_match(self):
        return round(self.goals + self.assists / self.games_played, 2) if self.games_played != 0 else 0

    @property
    def goals_against_average(self):
        return round(self.goals_given / self.shot_against, 2) if self.shot_against != 0 else 0
    
    @property
    def goals_against_per_match(self):
        return round(self.goals_given / self.games_played, 2) if self.games_played != 0 else 0
    
    @property
    def save_percentage(self):
        return round(self.shot_against / self.save, 2) if self.save != 0 else 0
    
    @property
    def save_per_match(self):
        return round(self.save / self.games_played, 2) if self.games_played != 0 else 0
    
    @property
    def penalty_per_match(self):
        return round(self.penalty_minutes / self.games_played, 2) if self.games_played != 0 else 0
    

    

    def to_dict(self):
        return {
            'games_played': self.games_played,
            'wins': self.wins,
            'losses': self.losses,
            'shot_against': self.shot_against,
            'save': self.save,
            'goals_given': self.goals_given,
            'time_on_ice': self.time_on_ice,
            'goals': self.goals,
            'assists': self.assists,
            'penalty_minutes': self.penalty_minutes,
            'points': self.points,
            'points_per_match': self.points_per_match,
            'goals_against_average': self.goals_against_average,
            'goals_against_per_match': self.goals_against_per_match,
            'save_percentage': self.save_percentage,
            'save_per_match': self.save_per_match,
            'penalty_per_match': self.penalty_per_match,
        }
    
    @classmethod
    def from_dict(cls, data):
        games_played = data.get('games_played', 0)
        wins = data.get('wins', 0)
        losses = data.get('losses', 0)
        save = data.get('save', 0)
        goals_given = data.get('goals_given', 0)
        time_on_ice = data.get('time_on_ice', 0)
        goals = data.get('goals', 0)
        assists = data.get('assists', 0)
        penalty_minutes = data.get('penalty_minutes', 0)
        
        return cls(
            games_played=games_played,
            wins=wins,
            losses=losses,
            save=save,
            goals_given=goals_given,
            time_on_ice=time_on_ice,
            goals=goals,
            assists=assists,
            penalty_minutes=penalty_minutes
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

        