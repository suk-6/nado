from db import DB


class Board:
    def __init__(self) -> None:
        self.db = DB()

    def createBoard(self, name, owner):
        try:
            self.db.createBoard(name, owner)
            return True
        except:
            return False

    def getBoard(self, boardID=None):
        return self.db.getBoard(boardID)

    def createPost(self, title, content, board, owner):
        try:
            self.db.createPost(title, content, owner, board)
            return True
        except:
            return False

    def getPost(self, postID=None):
        return self.db.getPost(postID)
