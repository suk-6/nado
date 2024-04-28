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
