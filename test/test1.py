import main.game as m
import unittest
import os


class Test(unittest.TestCase):
    login = None
    db = None

    @classmethod
    def setUp(self):
        self.login = m.Login()
        self.db = m.Database()


    def testCheckCredentials(self):
        self.assertEqual(self.login.checkCredentials('dksilv4', 'pw'), True)
        self.assertEqual(self.login.checkCredentials('dksilv4', 'p'), False)
        self.assertEqual(self.login.checkCredentials('dksilv', 'pw'), False)
        self.assertEqual(self.login.checkCredentials('dkslv4', 'w'), False)

    def testPopulationDB(self):
        self.login.populationDB('dksilv4')
        self.login.populationDB('test')
        self.assertEqual(os.path.isfile("../db/dksilv4.db"), True)
        self.assertEqual(os.path.isfile("../db/test.db"), True)

    def testNewUser(self):
        print('\n'+self.testNewUser.__name__.upper())
        try:
            self.db.newUser('Marcel', 'Mendes', 'marcypt', 'marcy@dksilv4.com', 'pass')
        except:
            pass
        print(self.db.outputTable('users', 'dksilv4'))

    def testNewHuman(self):
        print('\n'+self.testNewHuman.__name__.upper())
        human = ['Diogo', 'da Silva', '18', '12-10-1999', 'male', 0, 0, 0]
        self.db.newHuman('dksilv4', human)
        print(self.db.outputTable('Humans', 'dksilv4'))

