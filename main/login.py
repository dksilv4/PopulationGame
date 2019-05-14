import sqlite3
from sqlite3 import Error
import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.behaviors import DragBehavior
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.label import Label
import time

Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'position', 'auto')
Config.set('graphics', 'resizable', False)
Config.set('kivy', 'exit_on_escape', 1)
kivy.require('1.0.0')
from kivy.core.window import Window


class SignInWindow(BoxLayout, Screen):
    username = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validateUser(self):
        user = self.ids.usernameField
        pwd = self.ids.pwdField
        info = self.ids.info
        validation = self.checkCredentials(user.text, pwd.text)
        if validation == False:
            info.text = '[color=#FF0000]Username and/or password were incorrect[/color]'

        if validation == None:
            info.text = '[color=#FF0000]Please input credentials![/color]'
        if validation == True:
            info.text = '[color=#00FF00]Welcome![/color]'
            self.username = user.text
            self.populationDB()
            self.manager.current = 'game'
            time.sleep(.4)
            Window.maximize()
            Window.fullscreen = 'auto'

    def test(self):
        Window.maximize()
        self.manager.current = 'game'

    def checkCredentials(self, username, password):
        if username == '' or password == '':
            return None
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

    def populationDB(self):
        if os.path.isfile("../db/" + str(self.username) + ".db"):
            pass
        else:
            newPeople = [['Adam', '', '18', '00-00-0000', 'male', 0, 1, 1],
                         ['Eve', '', '18', '00-00-0000', 'male', 0, 1, 1]]

            self.addHumanTable()
            for people in newPeople:
                self.newHuman(people)

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

    def newHuman(self, human):
        conn = sqlite3.connect(r"../db/" + self.username + ".db")
        con = conn.cursor()
        query = "INSERT INTO Humans(Forename,Surname,Age,DOB,Gender,Married,Mother,Father) VALUES(?, ?,?,?,?,?,?,?)"
        con.execute(query,
                    [(human[0]), (human[1]), (human[2]), (human[3]), (human[4]), (human[5]), (human[6]), (human[7])])
        conn.commit()
        conn.close()

    def switchToRegister(self):
        self.manager.current = 'register'
        registerWinSizeX, registerWinSizeY = 600, 450
        Window.size = (registerWinSizeX, registerWinSizeY)

    def exit(self):
        App.get_running_app().stop()
        Window.close()


class RegisterWindow(BoxLayout, Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def exit(self):
        from kivy.core.window import Window
        App.get_running_app().stop()
        Window.close()

    def back(self):
        self.manager.current = 'login'


class Game(BoxLayout, Screen):
    pass


class Manager(ScreenManager):
    Login = ObjectProperty(None)
    Register = ObjectProperty(None)
    Game = ObjectProperty(None)


class LoginApp(App):
    def build(self):
        Window.size = (600, 450)
        Window.clearcolor = (1, 1, 1, 1)
        Window.borderless = False
        return Manager(transition=SlideTransition())


if __name__ == '__main__':
    LoginApp().run()