import { useLocalSearchParams } from 'expo-router';
import React, { useState } from 'react';
import { Button, Text, TextInput, View } from 'react-native';

export default function dailyInfo() {
    const { username } = useLocalSearchParams();
    const [caloriesEaten, setCaloriesEaten] = useState('');
    const [caloriesBurned, setCaloriesBurned] = useState('');
    const [waterConsumed, setWaterConsumed] = useState('');
    const [socialMediaHours, setSocialMediaHours] = useState('');
    const [hoursProductive, setHoursProductive] = useState('');
    const vals = {
        "username": username,
        "caloriesEaten": caloriesEaten,
        "caloriesBurned": caloriesBurned,
        "waterConsumed": waterConsumed,
        "socialMediaHours": socialMediaHours,
        "hoursProductive": hoursProductive
    }
    const run = () => {
        fetch('http://localhost:5001/dailyInfo', {
            method: "POST",
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify(vals)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log(error);
    })
    }
    return (
        <View>
            <Text>Input calories consumed:</Text>
            <TextInput value={caloriesEaten} onChangeText={setCaloriesEaten} />
            <Text>Input calories burned:</Text>
            <TextInput value={caloriesBurned} onChangeText={setCaloriesBurned} />
            <Text>Input water consumed:</Text>
            <TextInput value={waterConsumed} onChangeText={setWaterConsumed} />
            <Text>Input social media hours:</Text>
            <TextInput value={socialMediaHours} onChangeText={setSocialMediaHours} />
            <Text>Input hours productive:</Text>
            <TextInput value={hoursProductive} onChangeText={setHoursProductive}/>
            <Button title="Input information to get gameplay!" onPress={run}/>
        </View>
    )
}