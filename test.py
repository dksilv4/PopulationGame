import main
import unittest


class TestGame(unittest.TestCase):

    def testHumanCreation(self):
        x = main.Human(19, "Adam", "male", "Manuel", "Celeste")
        self.assertEqual(x.name,"Adam")
        self.assertEqual(x.age,19)

    def testHumanMarry(self):
        x = main.Human(19, "Adam", "male", "Manuel", "Celeste")
        y = main.Human(19, "Eve", "female", "Dad", "Mum")
        x.marry()
        self.assertIsNotNone(x.married)
        self.assertEqual(x.married.name,"Eve")
        self.assertEqual(y.married.name,"Adam")

    def testHumanProcreate(self):
        x = main.Human(19, "Adam", "male", "Manuel", "Celeste")
        y = main.Human(19, "Eve", "female", "Dad", "Mum")
        x.marry()
        x.procreate()
        self.assertEqual(x.children,y.children)
        y.procreate()
        self.assertEqual(x.children, y.children)
        for child in x.children:
            print(child.name)
            self.assertEqual(child.dad,x)
            self.assertEqual(child.mum,y)
            self.assertEqual(child.age,0)
            self.assertEqual(child.married,None)
            self.assertEqual(child.dad.name,'Adam')
            for i in child.children:
                print('>>>>'+i.name)

    def testGamePopulation(self):
        z= main.Game()
        x = main.Human(19, "Adam", "male", "Manuel", "Celeste")
        y = main.Human(19, "Eve", "female", "Dad", "Mum")
        x.marry()
        x.procreate()
        self.assertEqual(z.getPopulationValue(),3)
        print(z.getPopulation())
