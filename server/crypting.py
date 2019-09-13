import hashlib              # Hashlib for create pass
from database import *      # Our db to store some data

def validlog(user):         #Get usname validation for login
    return shfromlnit("Users", "useraut", "usrpass", user)
def validreg(user):         #Get usname validation for registration
    return shfromlnst("Users", "useraut", "usrnm", user)

def login(jelsz, user):         # Login case
    salt = "sajtoscsirke"        # Salt for hash
    hash = hashlib.sha512(salt.encode('utf-8') + user.encode('utf-8') + jelsz.encode('utf-8')).hexdigest()    # Hash with salt + usr name + pass
    loginuser = validlog(hash)              # Is hash valid?
    print(str(loginuser) + " loginuser")
    print(hash + " hash")
    if loginuser == True:
        return True
    else:
        return False

def register(jelsz, user):      # reg thread
    regdat = validreg(user)     # Is it a valid user?
    print(str(regdat) + " regdat")
    try:
        if(regdat == False):
            salt = "sajtoscsirke"
            hash = hashlib.sha512(salt.encode('utf-8') + user.encode('utf-8') + jelsz.encode('utf-8')).hexdigest()
            hash = str(hash)
            print(createln("Users", "useraut", "usrnm"))
            print(createln("Users", "useraut", "usrpass"))
            writetoln("Users", "useraut", "usrnm", user)
            writetoln("Users", "useraut", "usrpass", hash)
            print("Sikeres regisztrácio " + user)
            return True
        else:
            print("Hibás regisztráció")
            return False
    except:
        print("Error in register")
        return False


