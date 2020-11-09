import sqlite3
import re
import os
import sys
import schedule
import time

from utils import weekday_interpreter
from utils import shortcut_creator

class TaskScheduler:
    def __init__(self):
        self.root_dir = os.getcwd()
        self.lnk_dir = self.root_dir + "/shortcuts/"
        self.shortcut = shortcut_creator.shortcut()

    def db_load_CID(self, query):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cache = cursor.execute(query)
        data = [row[0] for row in cache.fetchall()]
        connection.close()
        return(data)

    def db_load_all(self, query):
        connection = sqlite3.connect("./resources/courselist.db")
        cursor = connection.cursor()
        cache = cursor.execute(query)
        data = cache.fetchall()
        connection.close()
        return(data)

    # Run singular course
    def run(self, courseID):
        CID = str(courseID)
        query = "SELECT * FROM courseTable WHERE CID=" + CID
        dataList = self.db_load_all(query)
        dataSet = dataList[0]
        print(dataSet)

        identifier = CID + dataSet[1]
        pwd = dataSet[3]

        week = weekday_interpreter.weekday(None, identifier, None, pwd, None, None)
        week.job()

    # Load all courses into schedule   
    def load(self):
        # Open config and parse 'number of courses'
        query = "SELECT CID FROM courseTable"
        data = self.db_load_CID(query)
        
        # Load data from database
        for ID in data:
            db = []
            query = "SELECT * FROM courseTable WHERE CID={}".format(ID)
            data = self.db_load_all(query)
            print("----------------------")

            for i, item in enumerate(data[0]):
                db.append(item)

            print(db)
            course = db[1]
            meetingID = db[2]
            password = db[3]
            weekDict = db[4]
            startTime = db[5]

            # Course Name Identifier (PRIMARY KEY)
            PKcourse = str(ID) + course

            # parse weekdays + number of days
            weekSchedule = re.split(',', weekDict)
            numDays = len(weekSchedule)
            print(weekSchedule)
            print(numDays)

            while True:
                # Check if shortcuts exist
                file = self.lnk_dir + PKcourse + ".lnk"
                print(file)

                file_exist = os.path.exists(file)
                print("file exists: " + str(file_exist))

                if file_exist:
                    # call week_interpret class
                    week = weekday_interpreter.weekday(numDays, PKcourse, meetingID, password, startTime, weekSchedule)
                    week.interpret()
                    print("Initialized  [ {} ]".format(course))
                    break
                else:
                    status = self.shortcut.create(PKcourse, meetingID)
                    print(status)
                    print("FILE DOES NOT EXITS")
                    if status:
                        pass
                    else:
                        print("ERROR")
                        break
                    
# Scheduler run 24/7     
    def start(self):
        schedule.run_pending()

# Clear schedule
    def clear(self):
        schedule.clear()
