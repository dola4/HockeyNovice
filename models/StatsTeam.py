from database.mongoDB import connection

db = connection()

class StatsTeam:
    def __init__(self, victory=0, defeat=0, defeat_in_OT=0):
        self.victory = victory
        self.defeat = defeat
        self.defeat_in_OT = defeat_in_OT

    @property
    def points(self):
        return self.victory * 2 + self.defeat_in_OT



    def to_dict(self):
        return {
            "victory": self.victory,
            "defeat": self.defeat,
            "defeat_in_OT": self.defeat_in_OT,
            "points": self.points
        }

    @classmethod
    def from_dict(cls, data):
        victory = data.get('victory', 0)
        defeat = data.get("defeat", 0)
        defeat_in_OT = data.get("defeat_in_OT", 0)
        return cls(
            victory=victory,
            defeat=defeat,
            defeat_in_OT=defeat_in_OT
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
