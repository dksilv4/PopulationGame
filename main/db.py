import sqlite3


def humanSampleTable():
    con.execute('''CREATE TABLE IF NOT EXISTS Humans (
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


def userSampleTable():
    con.execute('''CREATE TABLE IF NOT EXISTS users(
    userID integer PRIMARY KEY,
    Forename text NOT NULL,
    Surname text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL,
    passwordHash text NOT NULL
    )''')


def printUserTable():
    print(con.execute('''SELECT * FROM users''').fetchall())


def addSampleData():
    try:
        con.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
                    VALUES(1,'Diogo','da Silva','dksilv4','diogo.dk.silva@outlook.com','pw')''')
        conn.commit()
    except Exception:
        pass


if __name__ == '__main__':
    conn = sqlite3.connect(r"../db/users.db")
    con = conn.cursor()
    humanSampleTable()
    userSampleTable()
    addSampleData()
    printUserTable()
    con.close()
    conn.close()
