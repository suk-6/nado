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
