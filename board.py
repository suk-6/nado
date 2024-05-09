from db import DB


class Board:
    def __init__(self) -> None:
        self.db = DB()
        self.boardList = ["취업/진로", "요리", "건강", "문화 생활", "운동", "자유/기타"]

        if self.getBoard() == []:
            for board in self.boardList:
                self.createBoard(board)

    def createBoard(self, name):
        try:
            self.db.createBoard(name)
            return True
        except:
            return False

    def getBoard(self, boardID=None):
        return self.db.getBoard(boardID)

    def deleteBoard(self, id, password):
        return self.db.deleteBoard(id, password)

    def createPost(self, title, content, board, password):
        try:
            self.db.createPost(title, content, board, password)
            return True
        except:
            return False

    def getPost(self, postID=None, boardID=None):
        return self.db.getPost(postID, boardID)

    def getComment(self, postID):
        return self.db.getComment(postID)

    def addComment(self, postID, commentID, content):
        try:
            self.db.addComment(postID, commentID, content)
            return True
        except:
            return False
