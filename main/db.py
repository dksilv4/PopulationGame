import sqlite3


##########################User Database
def userSampleTable():
    userCon.execute('''CREATE TABLE IF NOT EXISTS users(
    userID integer PRIMARY KEY,
    Forename text NOT NULL,
    Surname text NOT NULL,
    username text NOT NULL UNIQUE,
    email text NOT NULL,
    passwordHash text NOT NULL
    )''')


def printUserTable():
    print(userCon.execute('''SELECT * FROM users''').fetchall())


def addSampleData():
    try:
        userCon.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
                    VALUES(1,'Diogo','da Silva','dksilv4','diogo.dk.silva@outlook.com','pw')''')
        conn.commit()
    except Exception:
        pass



if __name__ == '__main__':
    conn = sqlite3.connect(r"../db/users.db")
    userCon = conn.cursor()
    userSampleTable()
    addSampleData()
    printUserTable()
    userCon.close()
    conn.close()
