# import json
# from models import UserModel
import sqlite3


class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./data.splite", check_same_thread=False)
        self.cur = self.conn.cursor()

        if not self.isExistTable():
            self.createTable()

    def __del__(self) -> None:
        self.conn.close()

    def isExistTable(self):
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user'"
        )
        return self.cur.fetchone() is not None

    def createTable(self):
        self.cur.execute(
            """
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kakaoUID TEXT,
                image TEXT,
                nickname TEXT,
                region TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE board (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE post (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                board INTEGER,
                password TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE interviewq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE interviewa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                questionID INTEGER,
                answer TEXT,
                userID INTEGER
            )
            """
        )

        self.conn.commit()

    def createBoard(self, name):
        self.cur.execute("INSERT INTO board (name) VALUES (?)", (name,))
        self.conn.commit()

    def getBoard(self, boardID=None):
        if boardID is not None:
            self.cur.execute("SELECT * FROM board WHERE id = ?", (boardID,))
            data = self.cur.fetchone()
            return {
                "id": data[0],
                "name": data[1],
            }

        self.cur.execute("SELECT * FROM board")
        data = self.cur.fetchall()

        return [
            {
                "id": board[0],
                "name": board[1],
            }
            for board in data
        ]

    def createPost(self, title, content, board, password):
        self.cur.execute(
            "INSERT INTO post (title, content, board, password) VALUES (?, ?, ?, ?)",
            (title, content, board, password),
        )
        self.conn.commit()

    def getPost(self, postID=None):
        if postID is not None:
            self.cur.execute("SELECT * FROM post WHERE id = ?", (postID,))
            data = self.cur.fetchone()
            return {
                "id": data[0],
                "title": data[1],
                "content": data[2],
                "board": data[3],
            }

        self.cur.execute("SELECT * FROM post")
        data = self.cur.fetchall()

        return [
            {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "board": post[3],
            }
            for post in data
        ]

    def saveInterviewQ(self, question):
        self.cur.execute("INSERT INTO interviewq (question) VALUES (?)", (question,))
        self.conn.commit()

    def getInterviewQ(self, questionID=None):
        if questionID is not None:
            self.cur.execute("SELECT * FROM interviewq WHERE id = ?", (questionID,))
            data = self.cur.fetchone()
            return {
                "id": data[0],
                "question": data[1],
            }

        self.cur.execute("SELECT * FROM interviewq")
        data = self.cur.fetchall()

        return [
            {
                "id": interviewq[0],
                "question": interviewq[1],
            }
            for interviewq in data
        ]

    def deleteAllInterviewQ(self):
        self.cur.execute("DELETE FROM interviewq")
        self.cur.execute("UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'interviewq'")
        self.conn.commit()

    def saveInterviewA(self, questionID, answer, userID):
        self.cur.execute(
            "INSERT INTO interviewa (questionID, answer, userID) VALUES (?, ?, ?)",
            (questionID, answer, userID),
        )
        self.conn.commit()

    def getInterviewA(self, questionID, userID):
        self.cur.execute(
            "SELECT * FROM interviewa WHERE questionID = ? AND userID = ?",
            (questionID, userID),
        )
        data = self.cur.fetchall()

        return [
            {
                "id": interviewa[0],
                "questionID": interviewa[1],
                "answer": interviewa[2],
                "userID": interviewa[3],
            }
            for interviewa in data
        ]
