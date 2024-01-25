from bson.objectid import ObjectId

from database.mongoDB import connection

from models.Team import Team
from models.Player import Player
from models.StatsTeam import StatsTeam
from models.StatsPlayer import StatsPlayer

db = connection()

def create():
    team_id = Team.find_one_by_name("PATS")._id
    print(team_id)
    player1 = Player(team_id=team_id,
                     email="olivier@gmail.com",
                     password="123",
                     first_name="Olivier",
                     last_name="Marandola",
                     niveau="novice 3", 
                     number = 41, 
                     phone = "5142148292", 
                     position = "Player",
                     photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player1.create()

    player2 = Player(team_id=team_id,
                        email="zack@gmail.com",
                        password="123",
                        first_name="Zachary",
                        last_name="Chouinard-Labrie",
                        niveau="novice 3",
                        number = 40,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player2.create()

    player3 = Player(team_id=team_id,
                        email="Nolan@gmail.com",
                        password="123",
                        first_name="Nolan",
                        last_name="Labrie",
                        niveau="novice 3",
                        number = 30,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player3.create()

    player4 = Player(team_id=team_id,
                        email="Albert@gmail.com",
                        password="123",
                        first_name="Albert",
                        last_name="Levesque",
                        niveau="novice 3",
                        number = 1,
                        phone = "5142148292",
                        position = "Goaler",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player4.create()

    player5 = Player(team_id=team_id,
                        email="Béa@gmail.com",
                        password="123",
                        first_name="Béatrice",
                        last_name="Jurkowski",
                        niveau= "novice 3",
                        number = 00,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player5.create()

    player6 = Player(team_id=team_id,
                        email="Paul@gmail.com",
                        password="123",
                        first_name="Paul",
                        last_name="Gravel-Cofky",
                        niveau="novice 3",
                        number = 00,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player6.create()
    player7 = Player(team_id=team_id,
                        email="charle@gmail.com",
                        password="123",
                        first_name="Charles",
                        last_name="Bilodeau",
                        niveau="novice 3",
                        number = 00,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player7.create()
    player8 = Player(team_id=team_id,
                        email="miguel@gmail.com",
                        password="123",
                        first_name="Miguel",
                        last_name="Stone",
                        niveau="novice 3",
                        number = 00,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player8.create()
    player9 = Player(team_id=team_id,
                        email="sebastian@gmail.com",
                        password="123",
                        first_name="Sebastian",
                        last_name="James Crisi",
                        niveau="novice 3",
                        number = 00,
                        phone = "5142148292",
                        position = "Player",
                        photo_url = "media/images_joueurs/DVJL3683.JPG",
    )
    player9.create()

def find_one():
    player_id = "64f3aaab7b8f47f97ec5935b"
    player_id = ObjectId(player_id)
    player = Player.find_one(player_id).to_dict()
    print(player)

def find_one_by_email():
    player_email = "olivier@gmail.com"
    player = Player.find_one_by_email(player_email)
    print(player)


def find_one_by_number():
    player_number = 11
    player = Player.find_one_by_number(player_number).to_dict()
    print(player)

def find_all():
    players = Player.find_all()
    if players:
        for player in players:
            print(player.to_dict())
    else:
        print("No player found")


def update():
    player_id = "64f3aaab7b8f47f97ec5935b"
    player_id = ObjectId(player_id)
    team_id = Team.find_one_by_name("Canadiens")._id
    team_id = ObjectId(team_id)
    player_updated_try = Player.find_one(player_id)
    player_updated_try.first_name = "Olivier"
    player_updated = Player(team_id=team_id,
                            email="patate@gmail.com",
                            password="123",
                            first_name="Patate",
                            last_name="Giroux",
                            age= 7,
                            number = 11,
                            phone = "5142148292",
                            position = "Center",
                            photo_url = "media/images_joueurs/DVJL3683.JPG",
                            )
    print(player_updated_try.update(player_id))


def delete():
    player_id = "64f3aaac7b8f47f97ec59360"
    player_id = ObjectId(player_id)
    Player.delete(player_id)


def increment_stats():
    player_id = "64f3aaab7b8f47f97ec5935b" 
    player_id = ObjectId(player_id)
    player = Player.find_one(player_id)
    print(player.stats_player.to_dict())

    if player is not None:
        result = player.update_player_stats("increment_goaler", "assists" ) 
        print(f"Update Stats Result: {result}")
        print(player.stats_player.to_dict())
    else:
        print("Player not found.")




#create()
#find_one()
#find_one_by_email()
#find_one_by_number()
find_all()
#update()
#delete()

#increment_stats()