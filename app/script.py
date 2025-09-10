#This script will be used to both connect to port 5001, Store info into a database, collect info from
#the database, compare info from the day to both 1) expected values and 2) how well you've done compared
#to the rest of the week and will calculate the diff here

from flask import Flask, request
import sqlite3
import copy
from transformers import pipeline
import torch

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
    calsPerDay = data["calsEaten"] - data["calsBurned"]
    socialMeidaHours = data["socialMediaHrs"]
    waterDrank = data["waterDrank"]
    hrsProductive = data["hrsProductive"]
    cursor.execute('SELECT * FROM userInfo WHERE username = ? ', [username])
    row = cursor.fetchone()
    if (row):
        cursor.execute('INSERT INTO userInfo (calsIntaked, socialMediaHours, waterDrank, hrsProductive) VALUES (?, ?, ?, ?)', 
            [calsPerDay, socialMeidaHours, waterDrank, hrsProductive])
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
        "weelyInfo": ""
    }
    
    #insert into DB:
    cursor.execute('INSERT INTO dailyInfo (username, calsIntaked, socialMediaHours, waterDrank, hrsProductive)', 
                    [username, dailyData["cals"], dailyData["socialMediaHrs"], 
                     dailyData["waterDrank"], dailyData["hrsProductive"]])
    conn.commit()

    #Calculate changes and populate dicts
    def handleDifferences(actual, expected, toNormalDifferences):
        percentDiff = lambda actual, expected: (abs(actual-expected) / expected) * 100
        for i in range(0, len(actual)):
            if actual[i] < expected[i]:
                difference = percentDiff(actual[i], expected[i])
                toNormalDifferences[(list(toNormalDifferences.keys())[0])] += difference

            else:
                difference = percentDiff(actual[i], expected[i])
                toNormalDifferences[(list(toNormalDifferences.keys())[0])] -= difference
                toNormalDifferences[(list(toNormalDifferences.keys())[i])] += difference
    
    #populate daily dicts   
    cursor.execute('SELECT * FROM userInfo WHERE username = ?', (username))
    row = cursor.fetchone()
    if (row):
        actual = [dailyData["cals"], dailyData["socialMediaHrs"],  dailyData["waterDrank"], dailyData["hrsProductive"]]
        expected = [row["calsIntaked"], row["socialMediaHours"], row["waterDrank"], row["hrsProductive"]]
        handleDifferences(actual, expected, dailyToNormalDifferences)
        #populate throttle
        for keys in dailyToNormalDifferences.keys():
            if dailyToNormalDifferences[keys] > 15 and dailyToNormalDifferences[keys] < 30:
                dailyToNormalThrottle["one"].append(keys)
            elif dailyToNormalDifferences[keys] > 30 and dailyToNormalDifferences[keys] < 50:
                dailyToNormalThrottle["two"].append(keys)
            elif dailyToNormalDifferences[keys] >= 50:
                dailyToNormalThrottle["three"].append(keys)
        
        outputs["dailyInfo"] = dailyToNormalThrottle
        
    #Extract information about weekly information
    cursor.execute('SELECT * FROM dailyInfo WHERE username = ? ORDER BY id DESC LIMIT 1', (username))
    row = cursor.fetchone()
    if (row):
        if (row["id"] >= 7 and row["id"]%7 == 0):
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
            cursor.execute('SELECT * FROM userInfo WHERE username = ?', (username))
            row = cursor.fetchone()
            expected = [row["calsIntaked"], row["socialMediaHours"], row["waterDrank"], row["hrsProductive"]]
            actual = [weeklyData["calsIntaked"], weeklyData["socialMediaHours"], weeklyData["waterDrank"], 
                      weeklyData["hrsProductive"]]
            handleDifferences(actual, expected, weeklyToNormalDiferences)
            #Pulling informative AI prompts. Will video-rendering in future, text rendering for now
            prompt = (
                f"Weekly summary of user '{username}' :\n"
                f'''Deviation between expected calories intaked and actual calories intaked is {weeklyToNormalDiferences["calsIntakedDeviation"]}
                    Where the expects is above the actual'''
                f'''Deviation between expected Social Media Hours and actual social media hours is {weeklyToNormalDiferences["socialMediaDeviation"]}
                    Where the actual is above the expected'''
                f'''Deviation between expected water consumed and actual water consumed is {weeklyToNormalDiferences["watersConsumedDeviation"]}
                    Where the actual is below the expected'''
                f'''Deviation between expected hours productive and actual hours productive is {weeklyToNormalDiferences["hoursProductiveDeviation"]}
                    Where the actual is below the expected'''
                f'''Deviation between expected health/productivity activites and actual health/productivity activites is {weeklyToNormalDiferences["hoursProductiveDeviation"]}
                    Where the actual is above OR below the expected'''
                "Based on this information, please provide a detailed and comprehensive action plan, which motivates the user, showing them common " \
                "reasons for these flaws (especially comparing values which are very negative, and which may be contribting to the overall negative)" \
                "health/productivity scores"
            )
            model_id = "openai/gpt-oss-120b"
            pipe = pipeline(
                "text-generation",
                model=model_id,
                torch_dtype="auto",
                device_map="auto",
            )
            messages = [
                {"role": "user", 
                 f"content": {prompt}},
            ]
            ans = pipe(
                messages,
                max_new_tokens=600,
            )
            outputs["weelyInfo"] = ans
    return outputs

if __name__ == '__main__':
    data = {
        "username": "sid",
        "calsEaten": 10, 
        "socialMediaHrs": 1,
        "calsBurned": 200,
        "waterDrank": 4,
        "hrsProductive": 8
    }
    val = handle_post(data)
    print(val)
    #app.run(host='0.0.0.0', port=5001)


