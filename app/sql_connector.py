import sqlite3
import datetime
import os

class SQLconnector:
    def __init__(self):
        self.date = datetime.datetime.today().strftime('%d-%m-%Y')
        self.db_path = os.path.join(os.path.realpath(__file__), r"..\Counter.db")

    def save(self, classname, counting, weight, time, MET):        
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class, date, count, weight, time, MET)")
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
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class, date, count, weight, time, MET)")
        if classname == "":
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ?", (start_date, end_date))
        else:
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ? and class = ?", (start_date, end_date, classname))
        list = res.fetchall()
        con.close()
        return list