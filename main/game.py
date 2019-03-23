import sqlite3
from sqlite3 import Error
import os


class Database:
    def __init__(self):
        pass

    def outputTable(self, table, username):
        if table == 'users':
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            output = con.execute('''SELECT * FROM users''').fetchall()
            conn.close()
            return output
        if table == 'Humans':
            try:
                conn = sqlite3.connect(r"../db/" + username + ".db")
                con = conn.cursor()
                output = con.execute('''SELECT * FROM Humans''').fetchall()
                conn.close()
                return output
            except:
                self.addHumanTable(username)
                self.outputTable(table, username)

    def addUserTable(self):
        try:
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            con.execute('''CREATE TABLE IF NOT EXISTS users(
    userID integer PRIMARY KEY,
    Forename text NOT NULL,
    Surname text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL,
    passwordHash text NOT NULL
    )''')
        except Error as e:
            print(e)

    def addUserSampleData(self, table, *args):
        if table == 'users':
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            con.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
                    VALUES(1,'Diogo','da Silva','dksilv4','diogo.dk.silva@outlook.com','pw')''')
            conn.close()

    def addHumanTable(self, username):
        try:
            conn = sqlite3.connect(r"../db/" + username + ".db")
            con = conn.cursor()
            con.execute("""CREATE TABLE IF NOT EXISTS Humans (
            HumanID integer PRIMARY KEY,
            Forename text NOT NULL,
            Surname text NOT NULL,
            Age integer NOT NULL,
            DOB text NOT NULL,
            Gender text NOT NULL,
            Married integer NULL,
            Mother integer NOT NULL,
            Father integer NOT NULL,
            FOREIGN KEY (Married) REFERENCES Humans(HumanID),
            FOREIGN KEY (Mother) REFERENCES Humans(HumanID),
            FOREIGN KEY (Father) REFERENCES Humans(HumanID)
            )""")
            conn.commit()
            conn.close()
        except Error as e:
            return e

    def newUser(self, forename, surname, username, email, password):
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        query = "INSERT INTO users(Forename, Surname, username, email, passwordHash) VALUES(?, ?, ?,?,?)"
        con.execute(query, [(forename), (surname), (username), (email), (password)])
        conn.commit()
        conn.close()

    def newHuman(self, username, human):
        conn = sqlite3.connect(r"../db/" + username + ".db")
        con = conn.cursor()
        query = "INSERT INTO Humans(Forename,Surname,Age,DOB,Gender,Married,Mother,Father) VALUES(?, ?, ?,?,?,?,?,?,?)"
        con.execute(query,
                    [(human[0]), (human[1]), (human[2]), (human[3]), (human[4]), (human[5]), (human[6]), (human[7]),
                     (human[8])])
        conn.commit()
        conn.close()


class Login:

    def __init__(self):
        pass

    def checkCredentials(self, username, password):
        try:
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            results = con.execute("SELECT passwordHash FROM users WHERE username=?", (username,)).fetchall()
            conn.close()
            if password == results[0][0]:
                return True
            else:
                return False
        except Exception:
            return False

    def getCredentials(self):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        verified = self.checkCredentials(username, password)
        if verified:
            self.populationDB(username)

    def populationDB(self, username):
        if os.path.isfile("../db/" + username + ".db"):
            pass
        else:
            Database().addHumanTable(username)


class Register():

    def __init__(self):
        pass
