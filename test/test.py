import sqlite3
import os
import main.main as main
import unittest
from unittest.mock import patch


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global z, con, login
        z = main.Game()
        conn = sqlite3.connect(r"../db/users.db")
        con = conn.cursor()
        login = main.Login()

    def testObjectCreation(self):
        con.execute('''INSERT INTO Humans(HumanID,Forename,MiddleName,Surname,Age,DOB,Gender,Married,Mother,Father) 
        VALUES(1,'Diogo','Correia','da Silva',19,'12-10-1999','male','None','None','None');''')
        con.execute("SELECT Humans.Forename FROM Humans WHERE HumanID = 1;")
        results = con.fetchall()
        for human in results:
            self.assertEqual(''.join(human), "Diogo")

    def testUserCreation(self):
        con.execute('''INSERT INTO users(userID, Forename, Surname, username, email, passwordHash)
        VALUES(10,'Diogo','da Silva','dksilva','diogo.dk.silva@outlook.com','pw')''')
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
        login.checkCredentials('dksilv4','pw')
        self.assertEqual(os.path.isfile("../db/dksilv4.db"), True)

    def testUserVerification(self):
        self.assertEqual(login.verifyCredentials("dksilv4","pw"),"Login was successful!")
        self.assertEqual(login.verifyCredentials("dksilv4", "pwn"), "Invalid password or email!")







