import unittest
import sqlite3
import os
from datetime import datetime
from SQLconnector import SQLconnector

class TestSQLconnector(unittest.TestCase):
    
    def setUp(self):
        self.sql_conn = SQLconnector()
        if os.path.exists(self.sql_conn.dbpath):
            os.remove(self.sql_conn.dbpath)


    def test_save(self):
        # Test that data is saved to the database
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        con = sqlite3.connect(self.sql_conn.dbpath)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, self.sql_conn.date))
        listreturn = res.fetchall()
        self.assertEqual(len(listreturn), 1)
        row = listreturn[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
        con.close()

    def test_extractcalorieslist(self):
        # Test that data is extracted from the database
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        startdate = datetime.today().strftime('%d-%m-%Y')
        enddate = datetime.today().strftime('%d-%m-%Y')
        result = self.sql_conn.extractcalorieslist(startdate, enddate, classname)
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
    
    def test_extractcalorieslist2(self):
        # Test that data is extracted from the database for different date
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.date = '01-01-2020'
        self.sql_conn.save(classname, counting, weight, time, MET)
        startdate = datetime.today().strftime('%d-%m-%Y')
        enddate = datetime.today().strftime('%d-%m-%Y')
        result = self.sql_conn.extractcalorieslist(startdate, enddate, classname)
        self.assertEqual(len(result), 0)
        startdate = '01-01-2020'
        enddate = '01-01-2020'
        result = self.sql_conn.extractcalorieslist(startdate, enddate, classname)
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)

    def tearDown(self):
        os.remove(self.sql_conn.dbpath)
        del self.sql_conn

if __name__ == '__main__':
    unittest.main()