#This script will connect to port 5001, Store info into a database, collect info from
#the database, compare info from the day to both 1) expected values and 2) how well you've done compared
#to the rest of the week. This will be calculated, AI info will be sent back on weekly basis
from flask import Flask, request, jsonify
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
app = Flask(__name__)

@app.route('/register', methods=['POST'])
def handleRegistration():
    #Hangle the sqlite connection now
    conn = sqlite3.connect('userData.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    cursor.execute("SELECT * FROM userInfo WHERE username = ?", [username])
    row = cursor.fetchone()
    if (row):
        return jsonify({"result": 0})
    cursor.execute('INSERT INTO userInfo (username, password) VALUES (?, ?)', [username, password])
    conn.commit()
    conn.close()
    return jsonify({"result": 1})

@app.route('/loginInfo', methods=['POST'])
def handle_Login():
    #Handle the sqlite connection now
    conn = sqlite3.connect('userData.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = request.get_json()
    #test to print values out 
    print(data)
    username = data["username"]
    password = data["password"]
    cursor.execute('SELECT * FROM userInfo WHERE username = ?', [username])
    row = cursor.fetchone()
    if not row or row["password"] != password:
        return jsonify({"result": 0}) 
    else:
        return jsonify({"result": 1})

#comment back in 
@app.route('/firstInfo', methods=['POST'])
#Added in argument to check capability of handling
def handle_post():
    #commented out for now
    conn = sqlite3.connect('userData.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = request.get_json()
    username = data["username"]
    calsPerDay = int(data["calsEaten"]) - int(data["calsBurned"])
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
        return jsonify({"result": 1})
    else:
        return jsonify({"result": 0})

#comment back in 
@app.route('/dailyInfo', methods=['POST'])
def handleDailyPost():
    conn = sqlite3.connect('userData.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    data = request.get_json()
    #Test to see where data is pulled
    print("THIS IS THE INPUTTED INFORMATION", data)
    #test end
    username = data["username"]
    dailyData = {
        "calsIntaked": int(data["caloriesEaten"]) - int(data["caloriesBurned"]),
        "socialMediaHours": int(data["socialMediaHours"]),
        "waterDrank": int(data["waterConsumed"]),
        "hrsProductive": int(data["hoursProductive"])
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
        #TEST for printing out both vals
        print("this is the actual ", actual)
        print("this is the expected ", expected)
        #end TEST
        for i in range(0, len(actual)):
            #this is for the calculations within the calories intakes and social media hours, where the  less, the better
            if (i<2):
                #In the case where actual[i] is 0
                if actual[i] == 0:
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= 100
                elif expected[i] == 0:
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += 100
                elif actual[i] < expected[i]:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= difference
                else:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference
                    toNormalDifferences[(list(toNormalDifferences.keys())[i+1])] += difference
            #This is for the calculations within the water drank and hours productive where the more, the better
            else:
                #In the case where actual[i] is 0
                if actual[i] == 0:
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= 100
                elif expected[i] == 0:
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += 100
                elif actual[i] > expected[i]:
                    difference = percentDiff(actual[i], expected[i])  
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference
                else:
                    difference = percentDiff(actual[i], expected[i])
                    toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference
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
        #Only enter in the weekly informtion if there are 7 instances (where it is order by descending value)
        if (row["id"] >= 0) and (row["id"]%7 == 0):
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
    print(outputs["dailyInfo"])
    return jsonify({"result": outputs})

app.run(host='0.0.0.0', port=5001)


