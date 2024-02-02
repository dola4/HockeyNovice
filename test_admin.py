from bson.objectid import ObjectId

from models.Admin import Admin


def test_create():
    email = "@gmail.com"
    password = ""
    admin = Admin(email=email, password=password)
    admin.create()

def find_one():
    admin_id = ""
    admin = Admin.find_one(admin_id)
    if admin:
        print(admin.to_dict())
    else:
        print("Admin not found")


def find_one_by_email():
    email = ""
    admin = Admin.find_one_by_email(email)
    if admin:
        print(admin.to_dict())
    else:
        print("Admin not found")


def find_all():
    admins = Admin.find_all()
    if admins:
        for admin in admins:
            print(admin.to_dict())
    else:
        print("No admin found")

def update():
    admin_id = ""
    admin_id = ObjectId(admin_id)
    admin = Admin("alloPatate@gmail.com", '456')
    admin.update(admin_id)
    print(admin.to_dict())

def delete():
    admin_id = ""
    admin_id = ObjectId(admin_id)
    Admin.delete(admin_id)

test_create()
#find_one()
#find_one_by_email()
#find_all()
#update()
#delete()
