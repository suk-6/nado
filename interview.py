from db import DB


class Interview:
    def __init__(self) -> None:
        self.db = DB()
        self.deleteAllInterviewQuestion()
        with open("questions.txt", "r") as f:
            self.questions = f.readlines()
            for question in self.questions:
                self.saveInterviewQuestion(question)

    def saveInterviewQuestion(self, question):
        try:
            self.db.saveInterviewQ(question)
            return True
        except:
            return False

    def getInterviewQuestion(self, questionID=None):
        return self.db.getInterviewQ(questionID)

    def deleteAllInterviewQuestion(self):
        try:
            self.db.deleteAllInterviewQ()
            return True
        except:
            return False

    def saveInterviewAnswer(self, questionID, answer, userID):
        try:
            self.db.saveInterviewA(questionID, answer, userID)
            return True
        except:
            return False

    def getInterviewAnswer(self, questionID, userID):
        return self.db.getInterviewA(questionID, userID)
