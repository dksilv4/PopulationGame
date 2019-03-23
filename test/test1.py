import main.game as m
import unittest
import os


class Test(unittest.TestCase):
    login = None
    db = None
    register = None

    @classmethod
    def setUp(self):
        self.login = m.Login()
        self.db = m.DB()
        self.register = m.Register()
        self.db.reset()

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
        os.remove("../db/test.db")

    def testNewUser(self):
        table = self.db.outputTable('users','dksilv4')
        try:
            if table[1][0]==2 and table[1][1]=="Marcel":
                print('\n' + self.testNewUser.__name__.upper())
                print(table)
            else:
                print('\n' + self.testNewUser.__name__.upper())
                self.db.newUser('Marcel', 'Mendes', 'marcypt', 'marcy@dksilv4.com', 'pass')
                print(self.db.outputTable('users', 'dksilv4'))

        except:
            print('\n' + self.testNewUser.__name__.upper())
            self.db.newUser('Marcel', 'Mendes', 'marcypt', 'marcy@dksilv4.com', 'pass')
            print(self.db.outputTable('users', 'dksilv4'))


    def testNewHuman(self):
        table = self.db.outputTable('Humans', 'dksilv4')
        try:
            if table[0][0] == 1 and table[0][1]== 'Diogo':
                print('\n' + self.testNewUser.__name__.upper())
                print(table)
            else:
                print('\n'+self.testNewHuman.__name__.upper())
                human = ['Diogo', 'da Silva', '18', '12-10-1999', 'male', 0, 0, 0]
                self.db.newHuman('dksilv4', human)
                print(self.db.outputTable('Humans', 'dksilv4'))
        except:
            print('\n' + self.testNewHuman.__name__.upper())
            human = ['Diogo', 'da Silva', '18', '12-10-1999', 'male', 0, 0, 0]
            self.db.newHuman('dksilv4', human)
            print(self.db.outputTable('Humans', 'dksilv4'))

    def testCheckName(self):
        self.assertEqual(self.register.checkName('d'), False)
        self.assertEqual(self.register.checkName('diogo'), True)

    def testCheckUsername(self):
        self.assertEqual(self.register.checkUsername('dk'),'NoLen')
        self.assertEqual(self.register.checkUsername('dksilv4'), 'Taken')
        self.assertEqual(self.register.checkUsername('dksilva'), True)

    def testCheckEmail(self):
        self.assertEqual(self.register.checkEmail('d','d'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('@d.com','@d.com'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('d@d.com','d@d.com'), True)
        self.assertEqual(self.register.checkEmail('d', 'a'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('@d.com', '@a.com'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('d@d.com', 'dad.com'), 'NoMatch')
        self.assertEqual(self.register.checkEmail('diogo.dk.silva@outlook.com', 'diogo.dk.silva@outlook.com'), 'Used')


    def testCheckPassword(self):
        self.assertEqual(self.register.checkPassword('pw','pw'),['Invalid Len.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('paw', 'pw'), ['No Match.\n', 'Invalid Len.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Paw', 'pw'), ['No Match.\n', 'Invalid Len.\n', 'No Digits.\n'])
        self.assertEqual(self.register.checkPassword('password', 'pw'), ['No Match.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Password', 'pw'), ['No Match.\n', 'No Digits.\n'])
        self.assertEqual(self.register.checkPassword('password1','password1'), ['No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Password1','Password1'), True)

    def checkInputValidation(self):
        self.assertEqual(self.register.inputValidation('Diogo','da Silva','dksilva','d@d.com', 'd@d.com','Password1','Password1'), True)

    def testIsInfoInDB(self):
        self.assertEqual(self.db.isInfoInUsers('username','dksilv4'), True)
        self.assertEqual(self.db.isInfoInUsers('username','djenorengoerp'), False)
        self.assertEqual(self.db.isInfoInUsers('email', 'diogo.dk.silva@outlook.com'), True)
        self.assertEqual(self.db.isInfoInUsers('email', 'didthrtnla@outlook.com'), False)
