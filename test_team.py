from bson.objectid import ObjectId

from models.Team import Team

def create():
    team1 = Team(name="PATS")
    team1.create()

    #team2 = Team(name="Maple Leafs")
    #team2.create()

    #team3 = Team(name="Oilers")
    #team3.create()

    #team4 = Team(name="Jets")
    #team4.create()

    #team5 = Team(name="Flames")
    #team5.create()

    #team6 = Team(name="Canucks")
    #team6.create()

def find_one():
    team_id  = ""
    team_id = ObjectId(team_id)
    print(Team.find_one(team_id))

def find_one_by_name():
    team_name = "Canadiens"
    print(Team.find_one_by_name(team_name))

def find_all():
    print(Team.find_all())

def update():
    team_id = ""
    team_id = ObjectId(team_id)
    team = Team("Cannadiens")
    print(team.update(team_id))

def delete():
    team_id = ""
    team_id = ObjectId(team_id)
    print(Team.delete(team_id))

def update_stats():
    team_id = "64f35d65d651a629fb11d53b" 
    team_id = ObjectId(team_id)
    team = Team.find_one(team_id)

    if team is not None:
        result = team.update_stats("defeat_in_OT", "increment") 
        print(f"Update Stats Result: {result}")
    else:
        print("Team not found.")

def find_players_by_team():
    id = "659d6d95437f6c7a9e3c93a0"
    players = Team.find_players_by_team(id)
    for player in players:
        print(player)


#create()
#find_one()
#find_one_by_name()
#find_all()
#update()
#delete()
#update_stats()
#find_players_by_team()