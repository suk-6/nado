from moviepy.editor import VideoFileClip


class STT:
    def __init__(self, client) -> None:
        self._client = client

    def __call__(self, audioPath: str) -> str:
        with open(audioPath, "rb") as f:
            return self._client.audio.transcriptions.create(
                file=f,
                model="whisper-1",
            ).text

    def __del__(self) -> None:
        self._client.close()

    def mp4tomp3(self, id: str) -> str:
        try:
            video = VideoFileClip(f"/tmp/{id}.mp4")
            video.audio.write_audiofile(f"/tmp/{id}.mp3")
            video.close()

            return True
        except Exception as e:
            return False


if __name__ == "__main__":
    stt = STT()
    text = stt("test.mp3")
    print(text)
