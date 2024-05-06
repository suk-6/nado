from db import DB


class Interview:
    def __init__(self, client) -> None:
        self.db = DB()
        self._client = client
        self.deleteAllInterviewQuestion()
        with open("questions.txt", "r") as f:
            self.questions = f.readlines()
            for question in self.questions:
                self.saveInterviewQuestion(question)

    def interviewAnalysis(self, result):
        result = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the interview. Write a summary of the interview. to about 500 CHARACTERS. Write in Korean.",
                },
                {
                    "role": "user",
                    "content": str(result),
                },
            ],
        )

        return result.choices[0].message.content

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
