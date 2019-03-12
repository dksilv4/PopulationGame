import main.main as main
import unittest


class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        global x, y, z
        x = main.Human(19, "Adam", "male", "Manuel", "Celeste")
        y = main.Human(19, "Eve", "female", "Dad", "Mum")
        z = main.Game()

    def testHumanCreation(self):
        self.assertEqual(x.name,"Adam")
        self.assertEqual(x.age,19)

    def testHumanMarry(self):
        x.marry()
        self.assertIsNotNone(x.married)
        self.assertEqual(x.married.name,"Eve")
        self.assertEqual(y.married.name,"Adam")

    def testHumanProcreate(self):
        x.marry()
        x.procreate()
        self.assertEqual(x.children,y.children)
        y.procreate()
        self.assertEqual(x.children, y.children)
        for child in x.children:
            print("Child: " + child.name)
            self.assertEqual(child.dad,x)
            self.assertEqual(child.mum,y)
            self.assertEqual(child.age,0)
            self.assertEqual(child.married,None)
            self.assertEqual(child.dad.name,'Adam')
            for i in child.children:
                print('>>>>'+i.name)

    def testGamePopulation(self):
        x.marry()
        x.procreate()
        self.assertEqual(z.getPopulationValue(),3)

