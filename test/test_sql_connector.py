import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import unittest
import sqlite3
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
        self.sql_conn.save(classname, counting, weight, time, MET)
        res = cur.execute("SELECT * FROM counting where class = ? and date = ?", (classname, self.sql_conn.date))
        list_return = res.fetchall()
        self.assertEqual(len(list_return), 1)
        row = list_return[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting * 2)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time * 2)
        self.assertEqual(row[5], MET * 2)
        con.close()

    def test_extract_calories_list(self):
        # Test that data is extracted from the database, save with today's date
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
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
        # Test that data is extracted from the database, save with a specific date
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.date = '2020-01-01'
        self.sql_conn.save(classname, counting, weight, time, MET)
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        result = self.sql_conn.extract_calories_list(start_date, end_date, classname)
        self.assertEqual(len(result), 0)
        start_date = '2020-01-01'
        end_date = '2020-01-01'
        result = self.sql_conn.extract_calories_list(start_date, end_date, classname)
        self.assertEqual(len(result), 1)
        row = result[0]
        self.assertEqual(row[0], classname)
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], counting)
        self.assertEqual(row[3], weight)
        self.assertEqual(row[4], time)
        self.assertEqual(row[5], MET)
        
    def test_extract_calories_list3(self):
        # Test that data is extracted from the database for all 3 activities
        classname = 'pushup'
        counting = 10
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        classname = 'situp'
        counting = 20
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        classname = 'squat'
        counting = 30
        weight = 5
        time = 60
        MET = 3
        self.sql_conn.save(classname, counting, weight, time, MET)
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
        end_date = datetime.datetime.today().strftime('%Y-%m-%d')
        result = self.sql_conn.extract_calories_list(start_date, end_date)
        self.assertEqual(len(result), 3)
        row = result[0]
        self.assertEqual(row[0], 'pushup')
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], 10)
        self.assertEqual(row[3], 5)
        self.assertEqual(row[4], 60)
        self.assertEqual(row[5], 3)
        row = result[1]
        self.assertEqual(row[0], 'situp')
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], 20)
        self.assertEqual(row[3], 5)
        self.assertEqual(row[4], 60)
        self.assertEqual(row[5], 3)
        row = result[2]
        self.assertEqual(row[0], 'squat')
        self.assertEqual(row[1], self.sql_conn.date)
        self.assertEqual(row[2], 30)
        self.assertEqual(row[3], 5)
        self.assertEqual(row[4], 60)
        self.assertEqual(row[5], 3)


    def tearDown(self):
        os.remove(self.sql_conn.db_path)
        del self.sql_conn

if __name__ == '__main__':
    unittest.main()
