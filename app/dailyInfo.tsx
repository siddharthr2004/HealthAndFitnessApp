import { router, useLocalSearchParams } from 'expo-router';
import React, { useState } from 'react';
import { Button, Text, TextInput, View } from 'react-native';

export default function dailyInfo() {
    const { username } = useLocalSearchParams();
    console.log("This is the username from dailyInfo: ", username);
    const [caloriesEaten, setCaloriesEaten] = useState('');
    const [caloriesBurned, setCaloriesBurned] = useState('');
    const [waterConsumed, setWaterConsumed] = useState('');
    const [socialMediaHours, setSocialMediaHours] = useState('');
    const [hoursProductive, setHoursProductive] = useState('');
    const [message, setMessage] = useState('');
    const vals = {
        "username": username,
        "caloriesEaten": caloriesEaten,
        "caloriesBurned": caloriesBurned,
        "waterConsumed": waterConsumed,
        "socialMediaHours": socialMediaHours,
        "hoursProductive": hoursProductive
    }
    const run = () => {
        const calsEatenNum = Number(caloriesEaten);
        const socialMediaHrsNum = Number(socialMediaHours);
        const calsBurnedNum = Number(caloriesBurned);
        const waterDrankNum = Number(waterConsumed);
        const hrsProductiveNum = Number(hoursProductive);
        //Makes sure daily inputted value is of correct sequence
        if (
            caloriesEaten.trim() === '' || isNaN(calsEatenNum) || calsEatenNum < 0 ||
            socialMediaHours.trim() === '' || isNaN(socialMediaHrsNum) || socialMediaHrsNum < 0 ||
            caloriesBurned.trim() === '' || isNaN(calsBurnedNum) || calsBurnedNum < 0 ||
            waterConsumed.trim() === '' || isNaN(waterDrankNum) || waterDrankNum < 0 ||
            hoursProductive.trim() === '' || isNaN(hrsProductiveNum) || hrsProductiveNum < 0
        ) {
            setMessage("Please input a valid number for all fields!");
            return;
        }
        fetch('http://localhost:5001/dailyInfo', {
            method: "POST",
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify(vals)
        })
        .then(response => response.json())
        .then(data => {
            //first print out the data recieved back, handling is done later
            const toSendOne = data["result"]["dailyInfo"]["one"];
            const toSendTwo = data["result"]["dailyInfo"]["two"];
            const toSendThree = data["result"]["dailyInfo"]["three"];
            //hard-coded out so that you don't increase costs of token requests
            const toSendFour = data["result"]["weeklyInfo"];
            router.push({
                pathname: '/gamePlay',
                //change dailyInfo back this is just a test
                params: { 
                    dailyInfoOne: JSON.stringify(toSendOne), 
                    dailyInfoTwo: JSON.stringify(toSendTwo), 
                    dailyInfoThree: JSON.stringify(toSendThree), 
                    dailyInfoFour: JSON.stringify(toSendFour),
                    username: username 
                }
            })
        })
        .catch(error => {
            //error for catching incorrect information
            console.log(error);
        })
    }
    return (
        <View style={{flexDirection: 'column', alignItems: 'center'}}>
            <Text>Input calories consumed:</Text>
            <TextInput value={caloriesEaten} onChangeText={setCaloriesEaten} style={{borderWidth: 1, marginBottom: 10, width: 250}}/>
            <Text>Input calories burned:</Text>
            <TextInput value={caloriesBurned} onChangeText={setCaloriesBurned} style={{borderWidth: 1, marginBottom: 10, width: 250}}/>
            <Text>Input water consumed:</Text>
            <TextInput value={waterConsumed} onChangeText={setWaterConsumed} style={{borderWidth: 1, marginBottom: 10, width: 250}}/>
            <Text>Input social media hours:</Text>
            <TextInput value={socialMediaHours} onChangeText={setSocialMediaHours} style={{borderWidth: 1, marginBottom: 10, width: 250}}/>
            <Text>Input hours productive:</Text>
            <TextInput value={hoursProductive} onChangeText={setHoursProductive} style={{borderWidth: 1, marginBottom: 10, width: 250}}/>
            <Button title="Input information to get gameplay!" onPress={run}/>
            <Text style = {{color: 'red', marginTop: 10}}>{message}</Text>
        </View>
    )
}