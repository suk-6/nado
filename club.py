from db import DB


class Club:
    def __init__(self) -> None:
        self.db = DB()

    def createClub(self, name, image, owner):
        try:
            self.db.createClub(name, image, owner)
            return True
        except:
            return False

    def getClub(self, clubID=None):
        return self.db.getClub(clubID)

    def joinClub(self, clubID, userID):
        try:
            self.db.insertClubUsers(clubID, userID)
            return True
        except:
            return False
