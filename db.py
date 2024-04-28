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

        self.conn.commit()

    def createUser(self, kakaoUID):
        user = self.getUser(kakaoUID)
        if user is not None:
            return user

        self.cur.execute("INSERT INTO user (kakaoUID) VALUES (?)", (kakaoUID,))
        self.conn.commit()

        return self.getUser(kakaoUID)

    def updateUserNickname(self, kakaoUID, nickname):
        self.cur.execute(
            "UPDATE user SET nickname = ? WHERE kakaoUID = ?", (nickname, kakaoUID)
        )
        self.conn.commit()

    def updateUserRegion(self, kakaoUID, region):
        self.cur.execute(
            "UPDATE user SET region = ? WHERE kakaoUID = ?", (region, kakaoUID)
        )
        self.conn.commit()

    def getUser(self, userID):
        self.cur.execute("SELECT * FROM user WHERE id = ?", (userID,))
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
        self.cur.execute(
            "INSERT INTO club (name, image, owner) VALUES (?, ?, ?)",
            (name, image, owner),
        )
        self.conn.commit()

    def updateClubUsers(self, clubID, users):
        self.cur.execute("UPDATE club SET users = ? WHERE id = ?", (users, clubID))
        self.conn.commit()
