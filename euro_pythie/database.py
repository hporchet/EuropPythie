from datetime import datetime, date
from log import database as log
import sqlite3

DB = sqlite3.connect("EuroPythie.sqlite")
DATE_FORMAT = "%d-%m-%Y"


def clean() -> None:
    log.info("CLEAN DATABASE")
    cursor = DB.cursor()

    date_del = date.today()
    date_del = date_del.replace(year=(date_del.year - 1))
    cursor.execute(
        "DELETE FROM games WHERE date_creation < '"
        + date_del.strftime(DATE_FORMAT)
        + "'"
    )

    DB.commit()
    cursor.close()


def purge() -> None:
    log.info("Purge of DB")
    cursor = DB.cursor()

    cursor.execute("DELETE FROM GAMES")

    DB.commit()
    cursor.close()


# https://stackoverflow.com/a/4040168
def month_diff(d1: date, d2: date) -> int:
    """Return the number of months between d1 and d2,
    such that d2 + month_diff(d1, d2) == d1
    """
    return (12 * d1.year + d1.month) - (12 * d2.year + d2.month)


def init() -> None:
    cursor = DB.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS games (id integer primary key autoincrement, name text, date_creation date, players text)"
    )
    cursor.close()

    log.info("Database Ready")


def getGames() -> list:
    clean()
    cursor = DB.cursor()
    res = []

    raw_games = cursor.execute("SELECT * FROM games").fetchall()
    for raw_game in raw_games:
        res.append(Game(*raw_game))

    cursor.close()
    return res


def saveGames(name: str, date_creation: str, players: str) -> None:
    cursor = DB.cursor()

    cursor.execute(
        "INSERT INTO games (name, date_creation, players) VALUES (?, ?, ?)",
        (name, date_creation, players),
    )
    DB.commit()

    cursor.close()


class Game:
    def __init__(self, id: int, name: str, date_creation: str, players: str) -> None:
        self.id = id
        self.name = name
        self.date_creation = datetime.strptime(date_creation, DATE_FORMAT)
        self.players = players.split(",")

    def __str__(self) -> str:
        players = " ".join(self.players)
        if month_diff(self.date_creation, date.today()) > 3:
            format_str = "~~{}\t{}\t{}~~"
        else:
            format_str = "{}\t{}\t{}"
        return str.format(
            format_str,
            self.date_creation.strftime(DATE_FORMAT),
            self.name,
            players,
        )
