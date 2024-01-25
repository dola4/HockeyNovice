from database.mongoDB import connection
from bson.objectid import ObjectId, InvalidId
from twilio.rest import Client

db = connection()


class Invitation:
    def __init__(self, player_id, token, status, _id=None):
        self._id = _id
        self.player_id = player_id
        self.token = token
        self.status = status  # Par exemple : "envoyé", "accepté", "expiré"

    def to_dict(self):
        return {
            "_id": self._id,
            "player_id": self.player_id,
            "token": self.token,
            "status": self.status
        }
    
    def from_dict(self, invitation_dict):
        return {
            "_id": invitation_dict["_id"],
            "player_id": invitation_dict["player_id"],
            "token": invitation_dict["token"],
            "status": invitation_dict["status"]
        }
    
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
            invitation = db.invitations.find_one({"_id": invitation_id})
            if invitation:
                invitation = invitation.from_dict(invitation)
                return invitation
            else:
                return None
        except Exception as e:
            print(e)
            return None
              
        
    def find_all(self):
        try:
            invitations = db.invitations.find()
            if invitations:
                invitations = [invitation.from_dict(invitation) for invitation in invitations]
                return invitations
            else:
                return None
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
            invitation = db.invitations.find_one({"player_id": player_id})
            if invitation:
                return invitation["status"]
            else:
                return None
        except Exception as e:
            print(e)
            return None
    
    def send_by_sms(self, phone, email, mot2pass, token):
        account_sid = 'ACff28aa0dd26c23d51908ee5f61c77076'
        auth_token = 'ba01b0dd65210fb423ce0e457fb20276'
        my_twilio_phone = '+16098432075'
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
            twilio_format_phone = "+1" + phone
            try:
                message = client.messages.create(
                    body=body,
                    from_=my_twilio_phone,
                    to=twilio_format_phone
                )

                db.invitations.update_one({"_id": self._id}, {"$set": {"status": "envoye"}})
                return True
            except Exception as e:
                print(e)
                return False
        else:
            return False
        
        
            
