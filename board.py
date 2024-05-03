from db import DB


class Board:
    def __init__(self) -> None:
        self.db = DB()

        if self.getBoard() == []:
            boardList = ["취업/진로", "요리", "건강", "문화 생활", "운동", "자유/기타"]
            for board in boardList:
                self.createBoard(board)

    def createBoard(self, name):
        try:
            self.db.createBoard(name)
            return True
        except:
            return False

    def getBoard(self, boardID=None):
        return self.db.getBoard(boardID)

    def createPost(self, title, content, board, password):
        try:
            self.db.createPost(title, content, board, password)
            return True
        except:
            return False

    def getPost(self, postID=None):
        return self.db.getPost(postID)
