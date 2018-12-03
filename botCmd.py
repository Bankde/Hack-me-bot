import sqlite3
import os

MSG_HELP = """List of commands:
!help
    List commands
!listAll
    List all animals
!show <animal>
    Give description
!getFlag
    Give flag (Admin only)
!serverInfo
    Give server info (Dragonite only)
!addAdmin <id>
    Make user an admin (Dragonite only)
!hint
    Give you a hint.

Source_code:
  https://github.com/Bankde/Hack-me-bot"""

MSG_NO_DRAGONITE = "You're not Dragonite. Go away !!"
MSG_SEARCH_ERROR = "We cannot find this animal in our database"
MSG_NO_ADMIN = "You are not Admin. Go away !!"
MSG_ANIMAL_CMD = "Please specify animal: e.g. !show dog"

APP_DB = "app.db"

HINT_URL = "https://i.imgur.com/QPKpeJL.jpg"

def init():
    serverInfo = os.getenv('SERVER_INFO', None)
    conn = sqlite3.connect(APP_DB)
    cursor = conn.cursor()
    values = (serverInfo,)
    cursor.execute("UPDATE ServerInfo SET info=?", values)
    conn.commit()
    values = ("TestLogUser", "TestLogMsg", )
    cursor.execute("INSERT INTO MsgLog VALUES (?,?)", values)
    conn.commit()
    conn.close()

# Log userId and their msg here
def _msgLog(user, msg):
    conn = sqlite3.connect(APP_DB)
    cursor = conn.cursor()
    values = (user, msg,)
    # CREATE TABLE MsgLog (user TEXT, msg TEXT);
    cursor.execute("INSERT INTO MsgLog VALUES (?,?)", values)
    conn.commit()
    conn.close()

# Show animal description
def _showAnimal(animal):
    try:
        conn = sqlite3.connect(APP_DB)
        cursor = conn.cursor()
        # CREATE TABLE Animals (animal TEXT UNIQUE, description TEXT);
        cursor.execute("SELECT description FROM Animals WHERE animal='%s'" % (animal))
        all_data = cursor.fetchone()
        conn.close()
        if all_data == None or len(all_data) == 0:
            return MSG_SEARCH_ERROR
        else:
            return all_data[0]
    except:
        print("SQL error for arg: %s" % (animal))
        return None

# List every animals
def _listAnimal():
    conn = sqlite3.connect(APP_DB)
    cursor = conn.cursor()
    # CREATE TABLE Animals (animal TEXT UNIQUE, description TEXT);
    cursor.execute("SELECT animal FROM Animals")
    all_data = cursor.fetchall()
    conn.close()
    return ", ".join([data[0] for data in all_data])

# My own reminder
def _getServerInfo(user):
    if user.lower() == "dragonite":
        conn = sqlite3.connect(APP_DB)
        cursor = conn.cursor()
        # CREATE TABLE ServerInfo (info TEXT);
        cursor.execute("SELECT info FROM ServerInfo")
        all_data = cursor.fetchone()
        conn.close()
        return all_data[0]
    else:
        return MSG_NO_DRAGONITE

# You should ask Dragonite to add you to admin list
def _addAdmin(user, arg):
    if user.lower() == "dragonite":
        try:
            conn = sqlite3.connect(APP_DB)
            cursor = conn.cursor()
            values = (arg,)
            # CREATE TABLE Admins (user TEXT PRIMARY KEY);
            cursor.execute("INSERT INTO Admins VALUES (?)", values)
            conn.commit()
            conn.close()
            return "Successfully add %s into admin" % (arg)
        except:
            return "You're already an admin"
    else:
        return MSG_NO_DRAGONITE

# Flag is secret. No one besides admin should see it.
def _getFlag(user):
    conn = sqlite3.connect(APP_DB)
    cursor = conn.cursor()
    # CREATE TABLE Admins (user TEXT PRIMARY KEY);
    cursor.execute("SELECT user FROM Admins WHERE user='%s'" % (user))
    all_data = cursor.fetchone()
    conn.close()
    if all_data != None and len(all_data) == 1:
        flag = os.getenv('FLAG', None)
        return flag
    else:
        print("Alert: %s is not admin." % (user))
        return MSG_NO_ADMIN

def runCmd(message, user):
    _msgLog(user, message)
    if message.lower() == "help" or message.lower() == "!help":
        return MSG_HELP
    elif message == "!listAll":
        return _listAnimal()
    elif message == ("!show"):
        return MSG_ANIMAL_CMD
    elif message.startswith("!show "):
        return _showAnimal(message[6:])
    elif message == "!serverInfo":
        return _getServerInfo(user)
    elif message == "!getFlag":
        return _getFlag(user)
    elif message[:10] == "!addAdmin ":
        arg = message[10:]
        return _addAdmin(user, arg)
    elif message == "!hint":
        return HINT_URL
    else:
        return ""
