import os

def createdb(name):
    try:
        if not os.path.isdir('database/' + name):
            os.mkdir("database/" + name)
            return True
        else:
            return "DB already exist"
    except OSError:
        return "Os error except while create " + name + " db"

def getfrdb(name):
    try:
        d = 'database/' + name
        [os.path.join(d, o) for o in os.listdir(d)
         if os.path.isdir(os.path.join(d, o))]
        return d
    except:
        return"Error while listing db-s"

def deldb(name):
    try:
        os.rmdir("database/" + name)
        return True
    except OSError:
        return "Os error except while deleting db"

def createtb(dbname, name):
    try:
        if not os.path.isdir("database/" + dbname + "/" + name):
            os.mkdir("database/" + dbname + "/" + name)
            return True
        else:
            return "TB already exist"
    except OSError:
        return "Os error except while create " + name + " table"

def getfrtb(dbname, name):
    try:
        d = 'database/' + dbname + '/' + name
        [os.path.join(d, o) for o in os.listdir(d)
         if os.path.isdir(os.path.join(d, o))]
        return d
    except:
        return"Error while listing tables"

def deltb(dbname, name):
    try:
        os.rmdir("database/"+dbname + "/" + name)
        return True
    except:
        return "Error while deleting table"

def createln(dbname, tbname, name):
    try:
        if not os.path.isfile("database/" + dbname + "/" + tbname + "/" + name):
            with open("database/" + dbname + '/' + tbname + '/' + name, mode="w", encoding="utf-8") as f:
                return True
        else:
            return "File already exist"
    except:
        return "Error while creating line"

def writetoln(dbname, tbname, name, string):
    try:
        if os.path.isfile("database/" + dbname + "/" + tbname + "/" + name):
            with open("database/" + dbname + '/' + tbname + '/' + name, mode="a", encoding="utf-8") as f:
                f.write("\n" + string)
                return True
        else:
            createln(dbname, tbname, name)
            with open("database/" + dbname + '/' + tbname + '/' + name, mode="a", encoding="utf-8") as f:
                f.write("\n" + string)
                return True
    except:
        return "Error while creating line"

def shfromlnst(dbname, tbname, name, string): #Search with string
    try:
        with open("database/" + dbname + '/' + tbname + '/' + name, mode="r", encoding="utf-8") as f:
            s = f.read()
            print(string + " str shf")
            print(s + " item shf")
            if string in s:
                return True
            return False
    except:
        return "Error in shfromlnst"

def shfromlnit(dbname, tbname, name, integ): #Search with int
    try:
        with open("database/" + dbname + '/' + tbname + '/' + name, mode="r", encoding="utf-8") as f:
            a = f.read()
            if(integ in a):
                return True
            else:
                return False
    except:
        return "Error in shfromlnit"

def getfrln(dbname, tbname, name):
    path = 'database/' + dbname + '/' + tbname + '/' + name
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    files1 = ""
    for f in files:
        files1 += f + "\n"
    return files1

def delln(dbname, tbname, name):
    try:
        os.remove(dbname + '/' + tbname + '/' + name)
        return True
    except:
        return 'Error while deleting ln'