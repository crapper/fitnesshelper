import sqlite3
import datetime
from pathlib import Path

class SQLconnector:
    def __init__(self):
        now = datetime.datetime.now()
        self.date = now.date()
        self.db_path = Path(__file__).parent / "Counter.db"

    def save(self, classname, counting, weight, time, MET):        
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class TEXT, date TEXT, count INTEGER, weight REAL, time REAL, MET REAL)")
        if type(self.date) == datetime.date:
            self.date = self.date.strftime('%Y-%m-%d')
        else:
            self.date = datetime.datetime.strptime(self.date, '%Y-%m-%d').strftime('%Y-%m-%d')
        input_arg = (classname, self.date, counting, weight, time, MET)
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, self.date))
        list_return = res.fetchall()
        if len(list_return) == 0:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?, ?, ?)", input_arg)
        else:
            cur.execute("UPDATE counting set count = count + ? where class = ? and date = ?", (counting, classname, self.date))
            cur.execute("UPDATE counting set time = time + ? where class = ? and date = ?", (time, classname, self.date))
            cur.execute("UPDATE counting set MET = MET + ? where class = ? and date = ?", (MET, classname, self.date))
        con.commit()
        con.close()

    def extract_calories_list(self, start_date, end_date, classname = ""):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class TEXT, date TEXT, count INTEGER, weight REAL, time REAL, MET REAL)")
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        if classname == "":
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ?", (start_date, end_date))
        else:
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ? and class = ?", (start_date, end_date, classname))
        list = res.fetchall()
        con.close()
        return list
