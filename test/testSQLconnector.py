import sys
sys.path.insert(1, './')
#
import unittest
import sqlite3
import os
import datetime
# from SQLconnector import SQLconnector
from app import *

class TestSQLconnector(unittest.TestCase):
    
    def setUp(self):
        self.sql_conn = SQLconnector()
        if os.path.exists(self.sql_conn.db_path):
            os.remove(self.sql_conn.db_path)


    def test_save(self):
        # Test that data is saved to the database
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        con = sqlite3.connect(self.sql_conn.db_path)
        cur = con.cursor()
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, self.sql_conn.date))
        list_return = res.fetchall()
        self.assertEqual(len(list_return), 1)
        row = list_return[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
        con.close()

    def test_extract_calories_list(self):
        # Test that data is extracted from the database
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        start_date = datetime.datetime.today().strftime('%d-%m-%Y')
        end_date = datetime.datetime.today().strftime('%d-%m-%Y')
        result = self.sql_conn.extract_calories_list(start_date, end_date, classname)
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
    
    def test_extract_calories_list2(self):
        # Test that data is extracted from the database for different date
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.date = '01-01-2020'
        self.sql_conn.save(classname, counting, weight, time, MET)
        start_date = datetime.datetime.today().strftime('%d-%m-%Y')
        end_date = datetime.datetime.today().strftime('%d-%m-%Y')
        result = self.sql_conn.extract_calories_list(start_date, end_date, classname)
        self.assertEqual(len(result), 0)
        start_date = '01-01-2020'
        end_date = '01-01-2020'
        result = self.sql_conn.extract_calories_list(start_date, end_date, classname)
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)

    def tearDown(self):
        os.remove(self.sql_conn.db_path)
        del self.sql_conn

if __name__ == '__main__':
    unittest.main()