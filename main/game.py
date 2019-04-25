import os
import sqlite3
from sqlite3 import Error
import csv
import datetime
import random
import kivy


class DB:
    def __init__(self, username):
        self.username = username

    def reset(self):
        try:
            self.addUserTable()
            self.addUserSampleData()
            self.addHumanTable()
        except:
            pass

    def outputTable(self, db):
        if db == 'users':
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            output = con.execute('''SELECT * FROM users''').fetchall()
            conn.close()
            return output
        if db == 'Humans':
            try:
                conn = sqlite3.connect(r"../db/" + str(self.username) + ".db")
                con = conn.cursor()
                output = con.execute('''SELECT * FROM Humans''').fetchall()
                conn.close()
                return output
            except:
                self.addHumanTable()
                self.outputTable(db)

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

    def addHumanTable(self):
        try:
            conn = sqlite3.connect(r"../db/" + str(self.username) + ".db")
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

    def newHuman(self, human):
        conn = sqlite3.connect(r"../db/" + self.username + ".db")
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
        conn.close()
        if results == []:
            return False
        else:
            return True

    def getHuman(self):
        pass

    def getUserInfo(self, info):
        if info == 'name':
            query = """SELECT Forename, Surname FROM users WHERE username =?"""
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        data = con.execute(query, (self.username,)).fetchall()
        conn.close()
        return data

    @staticmethod
    def humanUpdateValue(column, newValue, nameColumn, humanName, ):
        conn = sqlite3.connect(r"../db/" + self.username + ".db")
        con = conn.cursor()
        query = """UPDATE Humans SET {} = {} WHERE {} = {}""".format(column, newValue, nameColumn, humanName)


class Login:
    verified = False
    username = None
    db = None

    def __init__(self, username=None):
        self.username = username
        self.db = DB(username)
        # self.getCredentials()

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

    def getCredentials(self, username=None, password=None):
        if username == None and password == None:
            user = input("Please enter your username: ")
            pw = input("Please enter your password: ")
            self.verified = self.checkCredentials(user, pw)
            if self.verified:
                self.username = user
                self.populationDB()
        else:
            self.verified = self.checkCredentials(username, password)
            if self.verified:
                self.username = username

    def populationDB(self):
        if os.path.isfile("../db/" + str(self.username) + ".db"):
            pass
        else:
            newPeople = [['Adam', '', '18', '00-00-0000', 'male', 0, 1, 1],
                         ['Eve', '', '18', '00-00-0000', 'male', 0, 1, 1]]

            self.db.addHumanTable()
            for people in newPeople:
                self.db.newHuman(people)

    def giveFeedback(self, info):
        if info == True:
            output = "Welcome {}!".format(' '.join(self.db.getUserInfo('name')[0]))
        print(output)
        return output



class Register:
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
            checkUsername = self.checkUsername(newInput)
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
        verified = checkForename and checkEmail and checkSurname and checkUsername and checkPassword
        if verified:
            self.forename = forename
            self.surname = surname
            self.email = email
            self.username = username
            self.password = password
            DB(self.username).newUser(self.forename, self.surname, self.username, self.email, self.password)
        return verified

    def checkName(self, name):
        if len(name) > 3:
            return True
        else:
            return False

    def checkUsername(self, username):
        if len(username) < 3:
            return 'NoLen'
        else:
            if DB(self.username).isInfoInUsers('username', username):
                return 'Taken'
            else:
                return True

    def checkEmail(self, email, emailVer):
        from validate_email import validate_email
        if validate_email(email):
            if email == emailVer:
                if DB(self.username).isInfoInUsers('email', email):
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


class Human:

    def __init__(self, id=0, forename=None, surname=None, age=0, dob=None, gender=None, mother=None, father=None,
                 married=None):
        self.id = id
        self.forename = forename
        self.surname = surname
        self.age = age
        self.dob = dob
        self.gender = gender
        self.mother = mother
        self.father = father
        self.married = married
        if gender == None:
            self.gender = self.getGender()
        if forename == None and surname == None:
            self.forename, self.surname = self.newName(self.gender)
        if dob == None:
            self.dob = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.mother = mother
        self.father = father
        self.married = married

    def newHuman(self):
        db.newHuman(username,
                    [self.forename, self.surname, self.surname, self.age, self.dob, self.gender, self.mother,
                     self.father, self.married])

    def __add__(self, mother, father):
        if mother.married == father.married:
            name = input("Please input the new human's name: ")
            surname = father.surname
            age = 0
            dob = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            gender = self.getGender()
            mother = mother
            father = father
            db.newHuman([None])

    def marry(self):
        pass

    def divorce(self):
        conn = sqlite3.connect(r"../db/" + self.username + ".db")
        con = conn.cursor()
        query = "UPDATE"


    def readNameCSV(self):
        with open('../csv/names.csv', newline='') as csvfile:
            maleNames = []
            femaleNames = []
            surnames = []
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in spamreader:
                info = ','.join(row)
                maleName, femaleName, surname = info.split(',')
                if maleName == 'MaleName':
                    continue
                else:
                    maleNames.append(maleName)
                    femaleNames.append(femaleName)
                    surnames.append(surname)
            return maleNames, femaleNames, surnames

    def newName(self, gender):
        maleNames, femaleNames, surnames = self.readNameCSV()
        randomInt = random.randint(0, len(maleNames) - 1)
        randomInt2 = random.randint(0, len(surnames) - 1)
        if gender == 'male':
            return maleNames[randomInt], surnames[randomInt2]
        if gender == 'female':
            return femaleNames[randomInt], surnames[randomInt2]

    def getGender(self):
        genders = ['male', 'female']
        return genders[random.randint(0, 1)]


class Game:
    population = []

    def __init__(self, username):
        self.username = username
        self.db = DB(username)
        self.loadPopulation()


    def loadPopulation(self):
        humans = self.db.outputTable('Humans')
        for human in humans:
            self.population.append(
                Human(human[0], human[1], human[2], human[3], human[4], human[5], human[6], human[7], human[8]))

    @property
    def showPopulation(self):
        for human in self.population:
            return ('{} {}\n '
                  '>Age: {} \n'
                  ' >Date of Birth: {}\n'
                  ' >Gender: {}\n'
                  ' >Mother: {}\n'
                  ' >Father: {}\n'
                  ' >Married to: {}\n'
                  '\n'.format(human.forename, human.surname, human.age, human.dob, human.gender, human.mother,
                              human.father, human.married))

    def updateHumanDB(self):
        pass

    def updateHumanAge(self):
        pass



if __name__ == '__main__':
    login = Login()
    username = login.username
    verified = login.verified
    if verified:
        db = DB(username)
        Game(username)
