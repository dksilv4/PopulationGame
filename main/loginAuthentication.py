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
