from datetime import datetime
from pathlib import Path

from dateutil import parser
from instabot import Bot


def is_today_file(file_name: str) -> bool:
    """Checks if filename contains today's date in it's name"""
    today = datetime.today().date()
    file_day = parser.parse(file_name).date()
    return file_day == today


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent
    out = BASE_DIR.joinpath("out")
    posted = out.joinpath("posted")

    for file in out.iterdir():
        if file.suffix == ".png" and is_today_file(file.stem):
            bot = Bot()
            bot.login(username="", password="")
            bot.upload_photo(str(file), caption=("#qotd"))
            file.rename(posted.joinpath(file.name))  # to avoid double posts
            break
    else:
        print("No file for today, Master")
