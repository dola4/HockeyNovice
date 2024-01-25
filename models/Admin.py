from database.mongoDB import connection
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

db = connection()

class Admin:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = _id

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            }

    def from_dict(self, admin_dict):
        self.email = admin_dict["email"]
        self.password = admin_dict["password"]
        self._id = admin_dict.get("_id", None)
        return self
        


    def create(self):
        try:
            print(self.email)
            if Admin.find_one_by_email(self.email) != "Admin not found" :
                return "Admin already exists"
            else:
                self.password = generate_password_hash(self.password)
                inserted = db.admins.insert_one(self.to_dict())
                self._id = str(inserted.inserted_id)
                return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def find_one(cls, admin_id):
        try:
            admin_data = db.admins.find_one({"_id": ObjectId(admin_id)})
            if admin_data:
                admin = cls(_id=str(admin_data['_id']), email=admin_data['email'], password=admin_data['password'])
                return admin
            else:
                return "Admin not found"
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_one_by_email(cls, email):
        try:
            admin_data = db.admins.find_one({"email": email})
            if admin_data:
                return cls(email=admin_data['email'], password=admin_data['password'])
            else:
                return "Admin not found"
        except Exception as e:
            print(e)
            return None

    @classmethod
    def find_all(cls):
        try:
            admins = db.admins.find()
            if admins:
                return [Admin(email=admin["email"], password=admin["password"]) for admin in admins]
            else:
                return "No admin found"
        except Exception as e:
            print(e)
            return None

    def update(self, admin_id):
        try:
            existing_admin = db.admins.find_one({"_id": ObjectId(admin_id)})
            if existing_admin:
                if not check_password_hash(existing_admin["password"], self.password):
                    self.password = generate_password_hash(self.password)
            db.admins.update_one({"_id": ObjectId(admin_id)}, {"$set": self.to_dict()})
            return True
        except Exception as e:
            print(e)
            return False


    @classmethod
    def delete(cls, admin_id):
        try:
            db.admins.delete_one({"_id": ObjectId(admin_id)})
            return True
        except Exception as e:
            print(e)
            return False
