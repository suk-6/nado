import random
import pdfkit


class Resume:
    def __init__(self, name, content) -> None:
        self.name = name
        self.content = content.split("\n")
        self.rand = random.randint(0, 1000000)
        self.html = self.convertHTML()
        self.savePDF()

        print(f"PDF saved at /tmp/{self.rand}.pdf")

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
		<style>
			* {{
				margin: 0;
				padding: 0;
				font-family: sans-serif;
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


if __name__ == "__main__":
    resume = Resume(
        "이름",
        "내용",
    )
