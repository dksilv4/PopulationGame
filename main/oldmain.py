import datetime
import random
import time
import sqlite3
import os
from sqlite3 import Error
import hashlib, binascii, os
from validate_email import validate_email


class Login:

    def __init__(self):
        self.con = self.createConnection()

    def createConnection(self):
        try:
            conn = sqlite3.connect(r"../db/users.db")
            con = conn.cursor()
            return con
        except Error as e:
            print(e)
        return None

    def inputCredentials(self):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        self.verifyCredentials(username, password)

    def verifyCredentials(self, username, password):
        verification = False
        while verification == False:
            verification = self.checkCredentials(username, password)
            self.username = username
            self.password = password
            if verification == True:
                self.userPopulationConnection()
                return "Login was successful!"
            if verification == False:
                return 'Invalid password or email!'

    def checkCredentials(self, username, password):
        try:
            results = self.con.execute("SELECT passwordHash FROM users WHERE username=?", (username,)).fetchall()
            if password == results[0][0]:
                return True
            else:
                return False
        except Exception:
            return False

    def userPopulationConnection(self):
        conn = sqlite3.connect(r"../db/" + str(self.username) + ".db")
        self.pCon = conn.cursor()
        self.humanSampleTable()
        return self.pCon

    def humanSampleTable(self):
        self.pCon.execute('''CREATE TABLE IF NOT EXISTS Humans (
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


class Register:
    conn = ''
    con = ''
    forename = ''
    surname = ''
    username = ''
    email = ''
    emailVer = ''
    password = ''
    passwordVer = ''
    passwordHash = ''

    def __init__(self):
        self.conn = self.createConnection()
        self.con = self.conn.cursor()

    def createConnection(self):
        try:
            return sqlite3.connect(r"../db/users.db")
        except Error as e:
            print(e)
        return None

    def getInputs(self):
        self.forename = input("Please enter your forename: ")
        self.surname = input("Please enter your surname: ")
        self.username = input("Please enter your username: ")
        self.email = input(" Please enter your email: ")
        self.emailVer = input("Please enter your email again: ")
        self.password = input(" Please enter your password: ")
        self.passwordVer = input(" Please enter your password again: ")
        self.checkInputs(self.forename, self.surname, self.username, self.email, self.emailVer,
                         self.password, self.passwordVer)

    def checkInputs(self, forename, surname, username, email, emailVer, password, passwordVer):

        verified = self.verifyInputs(forename, surname, username, email, emailVer, password, passwordVer)
        if verified:
            self.saveToDB(forename, surname, username, email, password)




    def verifyInputs(self, forename, surname, username, email, emailVer, password, passwordVer):

        if self.email != self.emailVer:
            while self.email != self.emailVer:
                self.email = input(" Please enter your email: ")
                self.emailVer = input("Please enter your email again: ")
        else:
            while password != passwordVer:
                self.password = input(" Please enter your password: ")
                self.passwordVer = input(" Please enter your password again: ")
        return email == emailVer and password == passwordVer and  validate_email(email)

    def saveToDB(self, forename, surname, username, email, password):
        query = "INSERT INTO users(Forename, Surname, username, email, passwordHash) VALUES(?, ?, ?,?,?)"
        self.con.execute(query,[(forename), (surname), (username), (email), (password)])

    def validateEmail(self, email):
        return validate_email(email)

class Game:
    population = []

    def __init__(self):
        pass

    def getPopulation(self):
        output = []
        for human in self.population:
            output.append(human.name + '\n')
            output.append('>Age: ' + str(human.age) + '\n')
            output.append('>Gender: ' + human.gender + '\n')
            if human.married != None:
                output.append('>Married to: ' + human.married.name + '\n')
            try:
                output.append('>Mother: ' + human.mum + '\n')
                output.append('>Father: ' + human.dad + '\n')
            except:
                output.append('>Mother: ' + human.mum.name + '\n')
                output.append('>Father: ' + human.dad.name + '\n')
            output.append('\n')
        print(''.join(output))
        return output

    def getPopulationValue(self):
        return len(self.population)

    def getFamilyTree(self):
        population = self.population
        for human in population:
            if human.married != None:
                print(human.name + '' + human.married.name)
                print("|")
                population.remove(human.married)
                if len(human.children) > 0:
                    for children in human.children:
                        if children.married != None:
                            print(children.name + '' + children.married.name)
                            print('|')
                            population.remove(children), population.remove(children.married)
                        if children.married == None:
                            print(children.name)
                            print('')
                            population.remove(children)
            else:
                print(human.name)
                print('')
            population.remove(human)

    def updateAge(self):
        while gameRunning:
            for human in self.population:
                timeDifference = datetime.datetime.now() - human.dob
                difference = divmod(timeDifference.days * 86400 + timeDifference.seconds, 60)
                human.age = difference[1]
                time.sleep(100)


class Human:
    nameFirst = ""
    nameMiddle = ""
    nameLast = ""
    age = None
    gender = None
    dob = None
    married = None
    mum = None
    dad = None
    children = []

    def __init__(self, age, name, gender, mum, dad):
        self.age = age
        self.name = name
        self.gender = gender
        self.dob = datetime.datetime.now()
        self.mum = mum
        self.dad = dad
        self.married = None
        self.children = []
        Game.population.append(self)

    def getHumanName(self):
        return self.name

    def getHumanAge(self):
        return self.age

    def marry(self):
        if self.age > 17:
            if self.married == None:
                for human in Game.population:
                    if human.gender != self.gender:
                        if human.age > 17:
                            if self.dad != human.dad:
                                if human.married == None:
                                    self.married = human
                                    human.married = self
            else:
                print("Human already married!")
        else:
            print("Human under aged!")

    def procreate(self):
        if self.married != None:
            gender = self.newGender()
            name = self.newName(gender)
            age = 0
            child = None
            if self.gender == 'male':
                child = self.newHuman(age, name, gender, self.married, self)
            if self.gender == 'female':
                child = self.newHuman(age, name, gender, self, self.married)
            self.children.append(child)
            self.married.children = self.children
        else:
            print(self.name + " has nobody to procreate with.")

    def outputInfo(self):
        print('Name: ' + str(self.name))
        print('Age: ' + str(self.age))
        print('Gender: ' + str(self.gender))
        print('DOB: ' + str(self.dob))
        if self.married == None:
            print('Status: Single')
        if self.married != None:
            print('Status: Married to ' + str(self.married.name))
        print('Mother: ' + str(self.mum))
        print('Father: ' + str(self.dad))
        if len(self.children) > 0:
            for child in self.children:
                print('Children: ' + ''.join(child.name) + '\n')

    @staticmethod
    def newHuman(age, name, gender, mum, dad):
        human = Human(age, name, gender, mum, dad)
        return human

    @staticmethod
    def newGender():
        genders = ['male', 'female']
        return genders[random.randint(0, (len(genders) - 1))]

    @staticmethod
    def newName(gender):
        gender = gender
        nameMale = ['Diogo', 'Miguel', 'Marcel', 'Konstantinos']
        nameFemale = ['Nataly', 'Maria', 'Diana']
        if gender == 'male':
            x = random.randint(0, len(nameMale) - 1)
            return nameMale[x]
        if gender == 'female':
            x = random.randint(0, len(nameFemale) - 1)
            return nameFemale[x]


def startGame():
    global gameRunning
    gameRunning = True
    game = Login()
    game.createConnection()


def populationIncrease(gameRunning, populationSize, populationMultiplier):
    for i in range(0, 100):
        loopDone = False
        loopTime = datetime.datetime.now() + datetime.timedelta(seconds=1)
        while loopDone == False:
            currentTime = datetime.datetime.now()
            if currentTime == loopTime:
                populationSize = populationSize * populationMultiplier
                roundedPopulation = round(populationSize)
                print(roundedPopulation)
                loopDone = True


startGame()
