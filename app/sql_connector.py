import sqlite3
import datetime
import os

class SQLconnector:
    def __init__(self):
        self.date = datetime.datetime.today().strftime('%d-%m-%Y')
        self.dbpath = os.path.join(os.path.realpath(__file__), r"..\Counter.db")

    def save(self, classname, counting, weight, time, MET):        
        con = sqlite3.connect(self.dbpath)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class, date, count, weight, time, MET)")
        inputarg = (classname, self.date, counting, weight, time, MET)
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, self.date))
        listreturn = res.fetchall()
        if len(listreturn) == 0:
            cur.execute("INSERT INTO counting VALUES (?, ?, ?, ?, ?, ?)", inputarg)
        else:
            cur.execute("UPDATE counting set count = count + ? where class = ? and date = ?", (counting, classname, self.date))
            cur.execute("UPDATE counting set time = time + ? where class = ? and date = ?", (time, classname, self.date))
            cur.execute("UPDATE counting set MET = MET + ? where class = ? and date = ?", (MET, classname, self.date))
        con.commit()
        con.close()

    def extractcalorieslist(self, startdate, enddate, classname = ""):
        con = sqlite3.connect(self.dbpath)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS counting(class, date, count, weight, time, MET)")
        if classname == "":
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ?", (startdate, enddate))
        else:
            res = cur.execute("SELECT * FROM counting where date BETWEEN ? and ? and class = ?", (startdate, enddate, classname))
        list = res.fetchall()
        con.close()
        return list