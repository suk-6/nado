import sqlite3


class DB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("./data.splite", check_same_thread=False)
        self.cur = self.conn.cursor()

        if not self.checkExistTable():
            self.createTable()

    def __del__(self) -> None:
        self.conn.close()

    def isExistTable(self):
        self.cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='user'"
        )
        return self.cur.fetchone() is not None

    def createTable(self):
        self.cur.execute(  # User Table
            """
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kakaoUID TEXT,
                image TEXT,
                nickname TEXT,
                region TEXT,
            )
            """
        )

        self.cur.execute(  # Club Table
            """
            CREATE TABLE club (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                image TEXT,
                owner INTEGER,
                users TEXT,
            )
            """
        )

        self.conn.commit()

    def createUser(self, kakaoUID):
        if self.getUser(kakaoUID) is not None:
            return

        self.cur.execute("INSERT INTO user (kakaoUID) VALUES (?)", (kakaoUID,))
        self.conn.commit()

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

    def getUser(self, kakaoUID):
        self.createUser(kakaoUID)

        self.cur.execute("SELECT * FROM user WHERE kakaoUID = ?", (kakaoUID,))
        return self.cur.fetchone()

    def createClub(self, name, image, owner):
        self.cur.execute(
            "INSERT INTO club (name, image, owner) VALUES (?, ?, ?)",
            (name, image, owner),
        )
        self.conn.commit()

    def updateClubUsers(self, clubID, users):
        self.cur.execute("UPDATE club SET users = ? WHERE id = ?", (users, clubID))
        self.conn.commit()
