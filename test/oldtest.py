import sqlite3
import os
import main.oldmain as main
import unittest
import time


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global z, con, login, register
        z = main.Game()
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        login = main.Login()
        register = main.Register()

    def testObjectCreation(self):
        con.execute('''INSERT INTO Humans(HumanID,Forename,MiddleName,Surname,Age,DOB,Gender,Married,Mother,Father) 
        VALUES(1,'Diogo','Correia','da Silva',19,'12-10-1999','male','None','None','None');''')
        con.execute("SELECT Humans.Forename FROM Humans WHERE HumanID = 1;")
        results = con.fetchall()
        for human in results:
            self.assertEqual(''.join(human), "Diogo")

    def testUserCreation(self):
        con.execute('''INSERT INTO users(Forename, Surname, username, email, passwordHash)
        VALUES('Diogo','da Silva','dksilva','diogo.dk.silva@outlook.com','pw')''')
        con.execute("SELECT * FROM users WHERE userID=10;")
        results = con.fetchall()
        for user in results:
            self.assertEqual(user[0], 10)
            self.assertEqual(user[1], 'Diogo')
            self.assertEqual(user[2], 'da Silva')
            self.assertEqual(user[3], 'dksilva')
            self.assertEqual(user[4], 'diogo.dk.silva@outlook.com')
            self.assertEqual(user[5], 'pw')

    def testLoginCredCheck(self):
        self.assertEqual(login.checkCredentials('dksilv4', 'pw'), True)
        self.assertEqual(login.checkCredentials('dksilv4', 'p'), False)
        self.assertEqual(login.checkCredentials('dk', 'pw'), False)

    def testUserPopulationConnection(self):
        login.verifyCredentials('dksilva', 'pwn')
        self.assertEqual(os.path.isfile("../db/dksilva.db"), False)
        login.verifyCredentials('dksilv4','pw')
        self.assertEqual(os.path.isfile("../db/dksilv4.db"), True)

    def testUserVerification(self):
        self.assertEqual(login.verifyCredentials("dksilv4","pw"),"Login was successful!")
        self.assertEqual(login.verifyCredentials("dksilv4", "pwn"), "Invalid password or email!")

    def testEmailValidation(self):
        self.assertEqual(register.validateEmail('diogo.dk.silva@outlook.com'), True)
        self.assertEqual(register.validateEmail('dd.com'), False)

    def testVerifyInputs(self):
        self.assertEqual(
            register.verifyInputs('test','test', 'test', 'test@test.com', 'test@test.com','pass','pass'),True)
        self.assertEqual(
            register.verifyInputs('test', 'test', 'test', 'test@test.com', 'testtest.com', 'pass', 'pass'),False)

    def testSaveToDB(self):
        register.saveToDB('test', 'test', 'test', 'test@test.com', 'pass')
        search = con.execute('''SELECT * FROM users''').fetchall()
        self.assertEqual(search[-1][1],'test')
        self.assertEqual(search[-1][2], 'test')
        self.assertEqual(search[-1][3], 'test')
        self.assertEqual(search[-1][4], 'test@test.com')
        self.assertEqual(search[-1][5], 'pass')

    def testFullRegisterProcess(self):
        searchLen = len(con.execute('''SELECT * FROM users''').fetchall()) + 1
        register.checkInputs('test','test', 'usertest'+str(searchLen), 'test@test.com', 'test@test.com','pass','pass')
        search = con.execute('''SELECT * FROM users''').fetchall()
        self.assertEqual(search[-1][1], 'test')
        self.assertEqual(search[-1][2], 'test')
        self.assertEqual(search[-1][3], 'usertest' + str(searchLen))
        self.assertEqual(search[-1][4], 'test@test.com')
