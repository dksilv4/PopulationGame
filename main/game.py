import sqlite3
from sqlite3 import Error
import os


class DB:
    def __init__(self):
        pass

    def reset(self):
        try:
            self.addUserTable()
            self.addUserSampleData()
            self.addHumanTable('dksilv4')
        except:
            pass

    def outputTable(self, db, username):
        if db == 'users':
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            output = con.execute('''SELECT * FROM users''').fetchall()
            conn.close()
            return output
        if db == 'Humans':
            try:
                conn = sqlite3.connect(r"../db/" + username + ".db")
                con = conn.cursor()
                output = con.execute('''SELECT * FROM Humans''').fetchall()
                conn.close()
                return output
            except:
                self.addHumanTable(username)
                self.outputTable(db, username)

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

    def addUserSampleData(self):
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        con.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
                    VALUES(1,'Diogo','da Silva','dksilv4','diogo.dk.silva@outlook.com','pw')''')
        conn.commit()
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
        query = "INSERT INTO Humans(Forename,Surname,Age,DOB,Gender,Married,Mother,Father) VALUES(?, ?,?,?,?,?,?,?)"
        con.execute(query,
                    [(human[0]), (human[1]), (human[2]), (human[3]), (human[4]), (human[5]), (human[6]), (human[7])])
        conn.commit()
        conn.close()

    def isInfoInUsers(self, dataType, data):
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        query = """SELECT * FROM users WHERE {} =?""".format(dataType)
        results = con.execute(query, (data,)).fetchall()
        if results == []:
            return False
        else:
            return True


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
            DB().addHumanTable(username)


class Register():
    forename = ''
    surname = ''
    username = ''
    email = ''
    emailVer = ''
    password = ''
    passwordVer = ''
    passwordHash = ''

    def __init__(self):
        pass

    def getInputs(self):
        self.forename = input("Please enter your forename: ")
        self.surname = input("Please enter your surname: ")
        self.username = input("Please enter your username: ")
        self.email = input(" Please enter your email: ")
        self.emailVer = input("Please enter your email again: ")
        self.password = input(" Please enter your password: ")
        self.passwordVer = input(" Please enter your password again: ")
        if self.inputValidation(self.forename, self.surname, self.username, self.email, self.emailVer,
                                self.password, self.passwordVer):
            pass

    def inputValidation(self, forename, surname, username, email, emailVer, password, passwordVer):
        checkForename = self.checkName(forename)
        while not checkForename:
            newInput = input("Invalid input. Please enter your forename again: ")
            checkForename = self.checkName(newInput)
            if checkForename:
                self.forename = newInput
        checkSurname = self.checkName(surname)
        while not checkSurname:
            newInput = input("Invalid input. Please enter your surname again: ")
            checkSurname = self.checkName(newInput)
            if checkSurname:
                self.surname = newInput
        checkUsername = self.checkUsername(username)
        while not checkUsername:
            if checkUsername == 'NoLen':
                print("Username has to be more than five characters.")
            if checkUsername == 'Taken':
                print("Username has been taken, please choose another one.")
            newInput = input("Please enter your username again: ")
            checkUsername = self.checkName(newInput)
            if checkUsername:
                self.username = newInput
        checkEmail = self.checkEmail(email, emailVer)
        while not checkEmail:
            if checkEmail == 'InvalidFormat':
                print("Wrong email format given.")
            if checkEmail == 'NoMatch':
                print("Emails provided don't match.")
            if checkEmail == 'Used':
                print("Email already in use, please choose another.")
            mail = input("Invalid input. Please enter your email again: ")
            mailVer = input("Please enter the email again: ")
            checkEmail = self.checkEmail(mail, mailVer)
            if checkEmail:
                self.email = mail
        checkPassword = self.checkPassword(password, passwordVer)
        while not checkPassword:
            print(''.join(checkPassword))
            pw = input("Invalid input. Please enter your password again: ")
            pwVer = input("Please enter the password again: ")
            checkPassword = self.checkPassword(pw, pwVer)
            if checkPassword:
                self.password = pw
        return checkForename and checkEmail and checkSurname and checkUsername and checkPassword

    def checkName(self, name):
        if len(name) > 3:
            return True
        else:
            return False

    def checkUsername(self, username):
        if len(username) < 3:
            return 'NoLen'
        else:
            if DB().isInfoInUsers('username', username):
                return 'Taken'
            else:
                return True

    def checkEmail(self, email, emailVer):
        from validate_email import validate_email
        if validate_email(email):
            if email == emailVer:
                if DB().isInfoInUsers('email', email):
                    return 'Used'
                else:
                    return True
            else:
                return 'NoMatch'
        else:
            return 'InvalidFormat'

    def checkPassword(self, password, passwordVer):
        errors = []
        import re
        if password != passwordVer:
            errors.append("No Match.\n")
        if len(password) < 5:
            errors.append('Invalid Len.\n')
        if re.search('[0-9]', password) is None:
            errors.append('No Digits.\n')
        if re.search('[A-Z]', password) is None:
            errors.append('No Capitals.\n')
        if password == passwordVer and errors == []:
            return True
        return errors


if __name__ == '__main__':
    pass
