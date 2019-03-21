import sqlite3

##########################User Database
class usersDB:
    def __init__(self):
        self.conn = sqlite3.connect(r"../db/users.db")
        self.con = self.conn.cursor()

    def userSampleTable(self):
        self.con.execute('''CREATE TABLE IF NOT EXISTS users(
        userID integer PRIMARY KEY,
        Forename text NOT NULL,
        Surname text NOT NULL,
        username text NOT NULL UNIQUE,
        email text NOT NULL,
        passwordHash text NOT NULL
        )''')

    def printUserTable(self):
        print(self.con.execute('''SELECT * FROM users''').fetchall())


    def addSampleData(self):
        try:
            self.con.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
                        VALUES(1,'Diogo','da Silva','dksilv4','diogo.dk.silva@outlook.com','pw')''')
            self.conn.commit()
        except Exception:
            pass


##########################User Population Database
class userPopulation:
    def __init__(self):
        conn = sqlite3.connect(r"../db/"+self+".db")
        self.con = conn.cursor()

    def humanSampleTable(self):
        self.con.execute('''CREATE TABLE IF NOT EXISTS Humans (
            HumanID integer PRIMARY KEY,
            Forename text NOT NULL,
            MiddleName text,
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
            )''')






