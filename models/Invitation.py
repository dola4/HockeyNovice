from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId
from twilio.rest import Client
from datetime import datetime, timedelta


db = connection()

ACCOUNT_SID = ''
AUTH_TOKEN = ''
TWILIO_PHONE = ''

class Invitation:
    def __init__(self, player_id, token, date, status, _id=None):
        self._id = _id
        self.player_id = player_id
        self.token = token
        self.date = date
        self.status = status # "envoyé", "accepté", "expiré"

    def to_dict(self):
        return {
            "_id": self._id,
            "player_id": self.player_id,
            "token": self.token,
            "date": self.date,
            "status": self.status
        }
    
    def from_dict(self, invitation_dict):
        self._id = invitation_dict["team_id"]
        self.player_id = invitation_dict["player_id"]
        self.token = invitation_dict["token"]
        self.date = invitation_dict["date"]
        self.status = invitation_dict["status"]
        
        return self
    
    
    def create(self):
        try:           
            invitation_dict = self.to_dict()
            invitation_dict.pop("_id", None)
            
            inserted_invitation = db.invitations.insert_one(invitation_dict)
            self._id = inserted_invitation.inserted_id
                        
            return True
        
        except Exception as e:
            print(e)
            return False
        
    def find_one(self, invitation_id):
        try:
            invitation = db.invitations.find_one({"_id": ObjectId(invitation_id)})
            if invitation:
                return self.from_dict(invitation)  # Utilisez self pour créer une instance de Invitation
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def find_all(self):
        try:
            invitations = db.invitations.find()
            return [self.from_dict(invitation) for invitation in invitations]  
        except Exception as e:
            print(e)
            return None
    
    
    
    @classmethod
    def find_one_by_player(cls, player_id):
        try:
            if not isinstance(player_id, ObjectId):
                player_id = ObjectId(player_id)
            invitation_dict = db.invitations.find_one({"player_id": player_id})
            if invitation_dict:
                return cls(**invitation_dict)
            else:
                return None
        except Exception as e:
            print(e)
            return None
        
    def update(self):
        try:
            db.invitations.update_one({"_id": self._id}, {"$set": self.to_dict()})
            return True
        except Exception as e:
            print(e)
            return False
        
    def delete(self, invitation_id):
        try:
            db.invitations.delete_one({"_id": invitation_id})
            return True
        except Exception as e:
            print(e)
            return False
        
    @classmethod
    def check_state(cls, player_id):
        try:
            invitation_dict = db.invitations.find_one({"player_id": ObjectId(player_id)})
            if invitation_dict:
                invitation = cls.from_dict(invitation_dict)  # Instanciez un objet Invitation
                if invitation.status == "envoye":
                    if invitation.date + timedelta(days=5) < datetime.now().date():
                        invitation.status = "expire"
                        invitation.update()  # Mettez à jour l'invitation dans la base de données
                        return "expire"
                return invitation.status
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    def send_by_sms(self, phone, email, mot2pass, token):
        account_sid = ACCOUNT_SID
        auth_token = AUTH_TOKEN
        my_twilio_phone = TWILIO_PHONE
        client = Client(account_sid, auth_token)

        body = f"""Bonjour,

        Vous avez été invité à rejoindre le jeu.

        connectez-vous avec votre email : {email}
        
        Votre mot de passe provisoire est : {mot2pass}

        Votre token est : {token}
        
        connectez vous dans les 5 jours suivant la réception de ce message pour valider votre inscription.

        Cordialement,
        L'équipe du jeu"""

        if self:
            player_twilio_format_phone = "+1" + phone
            try:
                message = client.messages.create(
                    body = body,
                    from_ = my_twilio_phone,
                    to = player_twilio_format_phone
                )

                db.invitations.update_one({"_id": self._id}, {"$set": {"status": "envoye"}})
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
        
        
            
 