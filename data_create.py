from DBCM import DBConnect
import json
from random import randint, random


today = 20231215
to_day = 20240201
startday = 20231101


class Time:
    def __init__(self, now):
        self.min = now % 100
        self.hour = now // 100

    def __str__(self):
        return f'{self.hour:02}:{self.min:02}:00'

    def __add__(self, other: int):
        ohour = self.hour
        omin = self.min + other % 60
        if omin >= 60:
            ohour = self.hour + omin // 60
            omin %= 60
        ohour += other // 60
        return Time(ohour*100+omin)

    def __ge__(self, other: int):
        omin = other % 100
        ohour = other // 100
        if self.hour > ohour:
            return True
        elif self.hour == ohour:
            if self.min >= omin:
                return True
            else:
                return False
        else:
            return False


with open('./json/root_db_config.json') as f:
    db_config = json.load(f)

with DBConnect(db_config) as cur:
    cur.execute("call recreate_table();")
    cur.execute("CREATE TRIGGER `seans_AFTER_INSERT` AFTER INSERT ON `seans` FOR EACH ROW call kino.generate_tickets(new.ID);")
    cur.execute("select ID, Duration from films")
    films = cur.fetchall()
    for i in range(1, 4):
        day = startday
        d = f'{day // 10000:04}-{(day // 100) % 100:02}-{day % 100:02}'
        t = Time(1000)
        while day < today:
            film = films[randint(0, 7)]
            if t+film[1] >= 2000:
                if day % 100 == 30:
                    day = day//100*100 + 101
                    if day % 10000 == 1301:
                        day = day//10000*10000 + 10101
                else:
                    day += 1
                d = f'{day // 10000:04}-{(day // 100) % 100:02}-{day % 100:02}'
                t = Time(1000)
            else:
                r = 1.0 + random()
                cur.execute(f"insert seans(Date, Time, film_ID, zal_ID, Ratio) values ('{d}', '{str(t)}', {film[0]}, {i}, {r:.2f})")
                t += film[1] + 10
        d = f'{day // 10000:04}-{(day // 100) % 100:02}-{day % 100:02}'
        while day <= to_day:
            film = films[randint(3, 11)]
            if t + film[1] >= 2000:
                if day % 100 == 30:
                    day = day // 100 * 100 + 101
                    if day % 10000 == 1301:
                        day = day//10000*10000 + 10101
                else:
                    day += 1
                d = f'{day // 10000:04}-{(day // 100) % 100:02}-{day % 100:02}'
                t = Time(1000)
            else:
                r = 1.0 + random()
                cur.execute(f"insert seans(Date, Time, film_ID, zal_ID, Ratio) values ('{d}', '{str(t)}', {film[0]}, {i}, {r:.2f})")
                t += film[1] + 10
    cur.execute("select ID from tickets")
    tickets = cur.fetchall()
    for tic in tickets:
        coin = randint(0, 3)
        if coin > 0:
            cur.execute(f"update tickets set Sold=True where ID = {tic[0]}")
