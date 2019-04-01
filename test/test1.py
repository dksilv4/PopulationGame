import main.game as game
import unittest
import os


class Test(unittest.TestCase):
    login = None
    db = None
    register = None
    human = None
    game = None

    @classmethod
    def setUp(self):
        self.login = game.Login('dksilv4')
        self.db = game.DB('dksilv4')
        self.register = game.Register()
        self.db.reset()
        self.human = game.Human()
        self.game = game.Game('dksilv4')

    def testCheckCredentials(self):
        self.assertEqual(self.login.checkCredentials('dksilv4', 'pw'), True)
        self.assertEqual(self.login.checkCredentials('dksilv4', 'p'), False)
        self.assertEqual(self.login.checkCredentials('dksilv', 'pw'), False)
        self.assertEqual(self.login.checkCredentials('dkslv4', 'w'), False)

    def testPopulationDB(self):
        self.login.populationDB()
        self.login.populationDB()
        self.assertEqual(os.path.isfile("../db/dksilv4.db"), True)
        self.assertEqual(os.path.isfile("../db/test.db"), False)

    def testNewUser(self):
        table = self.db.outputTable('users')
        try:
            if table[2][0] == 3 and table[2][1] == "Marcel":
                print('\n' + self.testNewUser.__name__.upper())
                print(table[2])
            else:
                print('\n' + self.testNewUser.__name__.upper())
                self.db.newUser('Marcel', 'Mendes', 'marcypt', 'marcy@dksilv4.com', 'pass')
                print(self.db.outputTable('users'))

        except:
            print('\n' + self.testNewUser.__name__.upper())
            self.db.newUser('Marcel', 'Mendes', 'marcypt', 'marcy@dksilv4.com', 'pass')
            print(self.db.outputTable('users'))

    def testNewHuman(self):
        table = self.db.outputTable('Humans')
        try:
            if table[0][0] == 1 and table[0][1] == 'Diogo':
                print('\n' + self.testNewHuman.__name__.upper())
                print(table[0])
            else:
                print('\n' + self.testNewHuman.__name__.upper())
                human = ['Diogo', 'da Silva', '18', '12-10-1999', 'male', 0, 0, 0]
                self.db.newHuman('dksilv4', human)
                print(self.db.outputTable('Humans'))
        except:
            print('\n' + self.testNewHuman.__name__.upper())
            human = ['Diogo', 'da Silva', '18', '12-10-1999', 'male', 0, 0, 0]
            self.db.newHuman('dksilv4', human)
            print(self.db.outputTable('Humans'))

    def testCheckName(self):
        self.assertEqual(self.register.checkName('d'), False)
        self.assertEqual(self.register.checkName('diogo'), True)

    def testCheckUsername(self):
        self.assertEqual(self.register.checkUsername('dk'), 'NoLen')
        self.assertEqual(self.register.checkUsername('dksilv4'), 'Taken')
        self.assertEqual(self.register.checkUsername('dksilv'), True)

    def testCheckEmail(self):
        self.assertEqual(self.register.checkEmail('d', 'd'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('@d.com', '@d.com'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('djerngoerg@d.com', 'djerngoerg@d.com'), True)
        self.assertEqual(self.register.checkEmail('d', 'a'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('@d.com', '@a.com'), 'InvalidFormat')
        self.assertEqual(self.register.checkEmail('d@d.com', 'dad.com'), 'NoMatch')
        self.assertEqual(self.register.checkEmail('diogo.dk.silva@outlook.com', 'diogo.dk.silva@outlook.com'), 'Used')

    def testCheckPassword(self):
        self.assertEqual(self.register.checkPassword('pw', 'pw'), ['Invalid Len.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('paw', 'pw'),
                         ['No Match.\n', 'Invalid Len.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Paw', 'pw'), ['No Match.\n', 'Invalid Len.\n', 'No Digits.\n'])
        self.assertEqual(self.register.checkPassword('password', 'pw'),
                         ['No Match.\n', 'No Digits.\n', 'No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Password', 'pw'), ['No Match.\n', 'No Digits.\n'])
        self.assertEqual(self.register.checkPassword('password1', 'password1'), ['No Capitals.\n'])
        self.assertEqual(self.register.checkPassword('Password1', 'Password1'), True)

    def testInputValidation(self):
        table = self.db.outputTable('users')
        try:
            if table[1][0] == 2 and table[1][1] == "Diogo":
                print('\n' + self.testInputValidation.__name__.upper())
                print(table[1])
            else:
                print('\n' + self.testInputValidation.__name__.upper())
                self.register.inputValidation('Diogo', 'da Silva', 'dksilva', 'd@d.com', 'd@d.com', 'Password1',
                                              'Password1')
                print(self.db.outputTable('users'))

        except:
            print('\n' + self.testInputValidation.__name__.upper())
            self.register.inputValidation('Diogo', 'da Silva', 'dksilva', 'd@d.com', 'd@d.com', 'Password1',
                                          'Password1')
            print(self.db.outputTable('users'))

    def testIsInfoInDB(self):
        self.assertEqual(self.db.isInfoInUsers('username', 'dksilv4'), True)
        self.assertEqual(self.db.isInfoInUsers('username', 'djenorengoerp'), False)
        self.assertEqual(self.db.isInfoInUsers('email', 'diogo.dk.silva@outlook.com'), True)
        self.assertEqual(self.db.isInfoInUsers('email', 'didthrtnla@outlook.com'), False)

    def testNewName(self):
        print('\n' + self.testNewName.__name__.upper())
        maleNames, femaleNames, surnames = self.human.readNameCSV()
        maleName, maleSurname = self.human.newName('male')
        femaleName, femaleSurname = self.human.newName('female')
        print('Male Name: {} {}'.format(maleName, maleSurname))
        print('Female Name: {} {}'.format(femaleName, femaleSurname))
        self.assertEqual(maleName in maleNames, True)
        self.assertEqual(femaleName in femaleNames, True)

    def testGameLoadPopulation(self):
        self.game.loadPopulation()
        testHuman = self.game.population[0]
        self.assertEqual(testHuman.forename,'Diogo')
        self.assertEqual(testHuman.surname, 'da Silva')
        self.assertEqual(testHuman.age, 18)
