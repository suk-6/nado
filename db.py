import json
import sqlite3
from models import UserModel


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
            CREATE TABLE club (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                image TEXT,
                owner INTEGER,
                users TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE board (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                owner INTEGER,
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE post (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                owner INTEGER,
                board INTEGER,
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE interviewq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE interviewa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                questionID INTEGER,
                answer TEXT,
                userID INTEGER,
            )
            """
        )

        self.conn.commit()

    def createUser(self, kakaoUID):
        user = self.getUser(kakaoUID=kakaoUID)
        if user is not None:
            return user

        self.cur.execute("INSERT INTO user (kakaoUID) VALUES (?)", (kakaoUID,))
        self.conn.commit()

        return self.getUser(kakaoUID=kakaoUID)

    def updateUserNickname(self, userID, nickname):
        self.cur.execute(
            "UPDATE user SET nickname = ? WHERE id = ?", (nickname, userID)
        )
        self.conn.commit()

    def updateUserRegion(self, userID, region):
        self.cur.execute("UPDATE user SET region = ? WHERE id = ?", (region, userID))
        self.conn.commit()

    def getUser(self, kakaoUID=None, userID=None):
        if userID is not None:
            self.cur.execute("SELECT * FROM user WHERE id = ?", (userID,))
        elif kakaoUID is not None:
            self.cur.execute("SELECT * FROM user WHERE kakaoUID = ?", (kakaoUID,))
        else:
            return None
        data = self.cur.fetchone()

        if data is None:
            return None

        return UserModel(
            id=data[0],
            kakaoUID=None,
            image=data[2],
            nickname=data[3],
            region=data[4],
        )

    def createClub(self, name, image, owner):
        users = json.dumps([owner])
        self.cur.execute(
            "INSERT INTO club (name, image, owner, users) VALUES (?, ?, ?, ?)",
            (name, image, owner, users),
        )
        self.conn.commit()

    def insertClubUsers(self, clubID, userID):
        club = self.getClub(clubID)
        users = club["users"]
        users.append(userID)
        users = json.dumps(users)

        self.cur.execute("UPDATE club SET users = ? WHERE id = ?", (users, clubID))
        self.conn.commit()

    def getClub(self, ClubID=None):
        if ClubID is not None:
            self.cur.execute("SELECT * FROM club WHERE id = ?", (ClubID,))
            data = self.cur.fetchone()
            return {
                "id": data[0],
                "name": data[1],
                "image": data[2],
                "owner": data[3],
                "users": json.loads(data[4]),
            }

        self.cur.execute("SELECT * FROM club")
        data = self.cur.fetchall()

        return [
            {
                "id": club[0],
                "name": club[1],
                "image": club[2],
                "owner": club[3],
                "users": json.loads(club[4]),
            }
            for club in data
        ]

    def createBoard(self, name, owner):
        self.cur.execute("INSERT INTO board (name, owner) VALUES (?, ?)", (name, owner))
        self.conn.commit()

    def getBoard(self, boardID=None):
        if boardID is not None:
            self.cur.execute("SELECT * FROM board WHERE id = ?", (boardID,))
            data = self.cur.fetchone()
            return {
                "id": data[0],
                "name": data[1],
                "owner": data[2],
            }

        self.cur.execute("SELECT * FROM board")
        data = self.cur.fetchall()

        return [
            {
                "id": board[0],
                "name": board[1],
                "owner": board[2],
            }
            for board in data
        ]

    def createPost(self, title, content, owner, board):
        self.cur.execute(
            "INSERT INTO post (title, content, owner, board) VALUES (?, ?, ?, ?)",
            (title, content, owner, board),
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
                "owner": data[3],
                "board": data[4],
            }

        self.cur.execute("SELECT * FROM post")
        data = self.cur.fetchall()

        return [
            {
                "id": post[0],
                "title": post[1],
                "content": post[2],
                "owner": post[3],
                "board": post[4],
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
