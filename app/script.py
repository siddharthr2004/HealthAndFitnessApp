#This script will be used to both connect to port 5001, Store info into a database, collect info from
#the database, compare info from the day to both 1) expected values and 2) how well you've done compared
#to the rest of the week and will calculate the diff here

from flask import Flask, request
import sqlite3
import copy
from transformers import pipeline
import torch
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv("keys.env")
apiKey = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = apiKey)

#FOR NOW WILL REMOVE THE APP ROUTING TO TEST CAPABILITY OF SCRIPT IN ITSELF
conn = sqlite3.connect('userData.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS userInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        username TEXT, 
        password TEXT,
        calsIntaked INTEGER,
        socialMediaHours INTEGER,
        waterDrank REAL,
        hrsProductive INTEGER
    )''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dailyInfo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, 
        calsIntaked INTEGER,
        socialMediaHours INTEGER,
        waterDrank REAL,
        hrsProductive INTEGER,
        FOREIGN KEY (username) REFERENCES userInfo(username)
    )''')
conn.commit()
#commented out for now
#app = Flask(__name__)
#comment back in 

#@app.route('/register', methods=['POST'])
def handleRegistration(data):
    #commented out for now
    #data = request.json
    username = data["username"]
    password = data["password"]
    cursor.execute("SELECT * FROM userInfo WHERE username = ?", [username])
    row = cursor.fetchone()
    if (row):
        return 0
    cursor.execute('INSERT INTO userInfo (username, password) VALUES (?, ?)', [username, password])
    conn.commit()
    return 1

#@app.route('/loginInfo', methods=['POST'])
#Added in argument to check capability of handling
def handle_Login(data):
    #commented out for now
    #data = request.json
    username = data["username"]
    password = data["password"]
    cursor.execute('SELECT * FROM userInfo WHERE username = ?', [username])
    row = cursor.fetchone()
    if not row or row["password"] != password:
        return 0
    else:
        return 1

#comment back in 
#@app.route('/firstInfo', methods=['POST'])
#Added in argument to check capability of handling
def handle_post(data):
    #commented out for now
    #data = request.json
    username = data["username"]
    calsPerDay = data["calsTotal"]
    socialMeidaHours = data["socialMediaHrs"]
    waterDrank = data["waterDrank"]
    hrsProductive = data["hrsProductive"]
    cursor.execute('SELECT * FROM userInfo WHERE username = ? ', [username])
    row = cursor.fetchone()
    if (row):
        cursor.execute('''UPDATE userInfo 
                       SET calsIntaked = ?, socialMediaHours = ?, waterDrank = ?, hrsProductive = ?
                       WHERE username = ?''', 
            [calsPerDay, socialMeidaHours, waterDrank, hrsProductive, username])
        conn.commit()
        return 1
    else:
        return 0

#comment back in 
#@app.route('/dailyInfo', methods=['POST'])
#Added in argument to check capability of handling
def handleDailyPost(data):
    #var initalization
    #commented out for now
    #data = request.json
    username = data["username"]
    dailyData = {
        "calsIntaked": data["calsEaten"] - data["calsBurned"],
        "socialMediaHours": data["socialMediaHrs"],
        "waterDrank": data["waterDrank"],
        "hrsProductive": data["hrsProductive"]
    }
    weeklyData = copy.deepcopy(dailyData)
    dailyToNormalThrottle = {
        #Range from 15-30
        "one": [],
        #range from 30-50
        "two": [],
        #range is 50+
        "three": []
    }
    dailyToNormalDifferences = {
        "TotalNormalizedDiff": 0,
        "calsIntakedDeviation": 0,
        "socialMediaDeviation": 0,
        "watersConsumedDeviation": 0,
        "hoursProductiveDeviation": 0
    }
    weeklyToNormalDiferences = copy.deepcopy(dailyToNormalDifferences)
    #vals to return:
    outputs = {
        "dailyInfo": {},
        "weeklyInfo": ""
    }
    
    #insert into DB:
    cursor.execute('INSERT INTO dailyInfo (username, calsIntaked, socialMediaHours, waterDrank, hrsProductive) VALUES (?, ?, ?, ?, ?)', 
                    [username, dailyData["calsIntaked"], dailyData["socialMediaHours"], 
                     dailyData["waterDrank"], dailyData["hrsProductive"]])
    conn.commit()

    #Calculate changes and populate dicts
    def handleDifferences(actual, expected, toNormalDifferences):
        percentDiff = lambda actual, expected: (abs(actual-expected) / expected) * 100
        for i in range(0, len(actual)):
            #this is for the calculations within the calories intakes and social media hours, where the  less, the better
            if (i<2):
                if actual[i] < expected[i]:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference
                else:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= difference
                    toNormalDifferences[(list(toNormalDifferences.keys())[i+1])] += difference
            #This is for the calculations within the water drank and hours productive where the more, the better
            else:
                if actual[i] > expected[i]:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference
                else:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= difference
                    toNormalDifferences[(list(toNormalDifferences.keys())[i+1])] += difference
        toNormalDifferences[(list(toNormalDifferences.keys())[0])] /= 4
        return toNormalDifferences
    
    #populate daily dicts   
    cursor.execute('SELECT * FROM userInfo WHERE username = ?', [username])
    row = cursor.fetchone()
    if (row):
        actual = [dailyData["calsIntaked"], dailyData["socialMediaHours"],  dailyData["waterDrank"], dailyData["hrsProductive"]]
        expected = [row["calsIntaked"], row["socialMediaHours"], row["waterDrank"], row["hrsProductive"]]
        dailyToNormal = handleDifferences(actual, expected, dailyToNormalDifferences)
        #populate throttle
        for key in dailyToNormalDifferences.keys():
            if dailyToNormal[key] > 15 and dailyToNormal[key] < 30:
                dailyToNormalThrottle["one"].append(key)
            elif dailyToNormal[key] > 30 and dailyToNormal[key] < 50:
                dailyToNormalThrottle["two"].append(key)
            elif dailyToNormal[key] >= 50:
                dailyToNormalThrottle["three"].append(key)
        outputs["dailyInfo"] = dailyToNormalThrottle
    #Extract information about weekly information
    cursor.execute('SELECT * FROM dailyInfo WHERE username = ? ORDER BY id DESC LIMIT 1', [username])
    row = cursor.fetchone()
    if (row):
        #Commenting this down to 0, replace bace to 7 when done with testing
        if (row["id"] >= 0): # and row["id"]%7 == 0):
            cursor.execute('SELECT * FROM dailyInfo WHERE id > ? AND id < ? AND username = ?', 
                            [row["id"]-7, row["id"], username])
            rows = cursor.fetchall()
            for row in rows:
                weeklyData["calsIntaked"] += row["calsIntaked"]
                weeklyData["socialMediaHours"] += row["socialMediaHours"]
                weeklyData["waterDrank"] += row["waterDrank"]
                weeklyData["hrsProductive"] += row["hrsProductive"]
            for key in weeklyData:
                weeklyData[key] /= 7
            #Iterate through keys in weeklyAvergae, find username, find diff b/w expected and 
            #weekly avg, place into throttle sections
            cursor.execute('SELECT * FROM userInfo WHERE username = ?', [username])
            row = cursor.fetchone()
            expected = [row["calsIntaked"], row["socialMediaHours"], row["waterDrank"], row["hrsProductive"]]
            actual = [weeklyData["calsIntaked"], weeklyData["socialMediaHours"], weeklyData["waterDrank"], 
                      weeklyData["hrsProductive"]]
            weeklyDifferencesAnswer = handleDifferences(actual, expected, weeklyToNormalDiferences)
            prompt = (
                f"Weekly summary of user '{username}' :\n"
                f'''Deviation between expected calories intaked and actual calories intaked is {weeklyDifferencesAnswer["calsIntakedDeviation"]}
                    Where the expects is above the actual'''
                f'''Deviation between expected Social Media Hours and actual social media hours is {weeklyDifferencesAnswer["socialMediaDeviation"]}
                    Where the actual is above the expected'''
                f'''Deviation between expected water consumed and actual water consumed is {weeklyDifferencesAnswer["watersConsumedDeviation"]}
                    Where the actual is below the expected'''
                f'''Deviation between expected hours productive and actual hours productive is {weeklyDifferencesAnswer["hoursProductiveDeviation"]}
                    Where the actual is below the expected'''
                f'''Deviation between expected health/productivity activites and actual health/productivity activites is {weeklyDifferencesAnswer["TotalNormalizedDiff"]}
                    Where the actual is above OR below the expected'''
                "Based on this information, please provide a detailed and comprehensive action plan, which motivates the user, showing them common " \
                "reasons for these flaws (especially comparing values which are very negative, and which may be contribting to the overall negative)" \
                "health/productivity scores"
            )

            response = client.responses.create(
                model="gpt-4o-mini",
                input=prompt
            )
            outputs["weeklyInfo"] += response.output_text
    return outputs

if __name__ == '__main__':
    
    registrationData = {
        "username": "Luke",
        "password": "12345"
    }
    firstTimData = {
        "username": "Luke",
        "calsTotal": 2100,
        "socialMediaHrs": 3,
        "waterDrank": 8,
        "hrsProductive": 7
    }
    dailyData = {
        "username": "Luke",
        "calsEaten": 40000, 
        "calsBurned": 80,
        "socialMediaHrs": 9,
        "waterDrank": 3,
        "hrsProductive": 5
    }
    val3 = handleDailyPost(dailyData)
    print("THIS IS THE DAILY INFO")
    print(val3["dailyInfo"])
    print("THIS IS THE WEEKLY INFO")
    print(val3["weeklyInfo"])
    #app.run(host='0.0.0.0', port=5001)


