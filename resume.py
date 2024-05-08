import random
import pdfkit
import requests
from openai import OpenAI
from config import getENV


class ResumePDF:
    def __init__(self, name, content) -> None:
        self.name = name
        self.content = content.split("\n")
        self.rand = random.randint(100000, 999999)
        self.html = self.convertHTML()
        self.savePDF()

    def getID(self):
        return self.rand

    def convertHTML(self):
        content = ""
        for c in self.content:
            content += f"<p>{c}</p>"

        return f"""
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta
			name="viewport"
			content="width=595px, initial-scale=1.0, height=842px"
		/>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap" rel="stylesheet">
		<style>
			* {{
				margin: 0;
				padding: 0;
				font-family: 'Nanum Gothic';
			}}

			body {{
				background-color: #ffffff;
			}}

			#resume {{
				margin: 40px;
				padding-top: 40px;
			}}

			#title {{
				font-weight: 700;
				font-size: 35px;
			}}

			#line {{
				width: 500px;
				height: 0px;
				border: 2px black solid;
				margin-top: 10px;
				margin-bottom: 25px;
			}}

			#content {{
				font-size: 16px;
				line-height: 1.5;
			}}

			#content p {{
				margin-bottom: 20px;
			}}
		</style>
	</head>
	<body>
		<div id="resume">
			<span id="title">{self.name}</span>
			<div id="line"></div>
			<div id="content">{content}</div>
		</div>
	</body>
</html>
"""

    def savePDF(self):
        pdfkit.from_string(
            self.html,
            f"/tmp/{self.rand}.pdf",
            options={
                "page-size": "A4",
                "encoding": "UTF-8",
                "margin-bottom": "0",
                "margin-right": "0",
                "margin-left": "0",
                "margin-top": "0",
                "disable-smart-shrinking": True,
                "page-width": "595px",
                "page-height": "842px",
            },
        )


class ResumeAI:
    def __init__(self, client) -> None:
        self._client = client
        self.model = "gpt-3.5-turbo"

    def generateResume(self, keywords):
        response = self._client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "Create a personal statement for the user. Keep it to about 500 CHARACTERS. The user provides keywords. Write in Korean.",
                },
                {
                    "role": "user",
                    "content": keywords,
                },
            ],
        )

        return response.choices[0].message.content


class Resume:
    def __init__(self, client) -> None:
        self._client = client

    def pdf(self, name, content):
        return ResumePDF(name, content)

    def generateResume(self, keywords):
        return ResumeAI(self._client).generateResume(keywords)

    def checkSpelling(self, orignalContent):
        try:
            content = orignalContent
            res = requests.post(
                getENV("SPELLING_CHECKER_URL"),
                json={"text": orignalContent},
            )
            print(res.json())
            for r in res.json():
                content = content.replace(r["token"], r["suggestions"][0])

            return content
        except Exception as e:
            return orignalContent


if __name__ == "__main__":
    print(
        f"/tmp/{Resume().pdf('홍길동', ResumeAI().generateResume('장점, 성실함, 긍정적, 활발, 사교성, 개발, 파이썬')).getID()}.pdf"
    )
