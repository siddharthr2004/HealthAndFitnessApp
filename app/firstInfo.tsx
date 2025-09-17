//File used for getting users expected values for health/productivity
import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Text, TextInput, TouchableOpacity, View } from 'react-native';

export default function AboutScreen() {
    const router = useRouter();
    const [message, setMessage] = useState('');
    const { firstUsername } = useLocalSearchParams();
    const [calsEaten, setCalsEaten] = useState('');
    const [socialMediaHrs, setSocialMediaHrs] = useState('');
    const [calsBurned, setCalsBurned] = useState('')
    const [waterDrank, setWaterDrank] = useState('')
    const [hrsProductive, setHrsProductive] = useState('');
    const vals = {
      "username": firstUsername,
      "calsEaten": calsEaten, 
      "socialMediaHrs": socialMediaHrs,
      "calsBurned": calsBurned,
      "waterDrank": waterDrank,
      "hrsProductive": hrsProductive
    };
    const run = () => {
        //first convert into int values to check if they exist and if they're 0
        const calsEatenNum = Number(calsEaten);
        const socialMediaHrsNum = Number(socialMediaHrs);
        const calsBurnedNum = Number(calsBurned);
        const waterDrankNum = Number(waterDrank);
        const hrsProductiveNum = Number(hrsProductive);
        //then do the if check
        if (
          isNaN(calsEatenNum) || calsEatenNum <= 0 ||
          isNaN(socialMediaHrsNum) || socialMediaHrsNum <= 0 ||
          isNaN(calsBurnedNum) || calsBurnedNum <= 0 ||
          isNaN(waterDrankNum) || waterDrankNum <= 0 ||
          isNaN(hrsProductiveNum) || hrsProductiveNum <= 0
        ) {
          setMessage("Please input a positive number for all fields!");
          return;
        }
        fetch('http://localhost:5001/firstInfo', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(vals),
        })
        .then(response => response.json())
        .then(data => {
          if (data["result"] == 0) {
            setMessage("Your data was not able to be inputted. Sorry for the inconvinience");
          } else {
            router.back()
          }
        })
        .catch(error => {
          console.log(error);
        })
        return;
      };
    return (
        <View style={{padding:20}}>
          <Text>Enter goal for calories ingested per-day:</Text>
          <TextInput value={calsEaten} onChangeText={setCalsEaten} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter goal for hours spent on social media per-day:</Text>
          <TextInput value={socialMediaHrs} onChangeText={setSocialMediaHrs} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter goal for calories burned per-day:</Text>
          <TextInput value={calsBurned} onChangeText={setCalsBurned} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter goal for daily water consumptiopn in cups per-day:</Text>
          <TextInput value={waterDrank} onChangeText={setWaterDrank} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter goal for hours productive per-day:</Text>
          <TextInput value={hrsProductive} onChangeText={setHrsProductive} style={{borderWidth: 1, marginBottom: 10}}/>
          <TouchableOpacity
            style={{
            padding: 16,
            borderWidth: 2,           
            borderColor: '#2196F3',   
            borderRadius: 8,          
            backgroundColor: 'white',
            alignItems: 'center',
            margin: 10,
            }}
            onPress={run}
          >
            <Text style={{ color: '#2196F3', fontWeight: 'bold' }}>Click here to input information and go back to login!</Text>
          </TouchableOpacity>
          <Text style={{color: 'red', marginTop: 10}}>{message}</Text>
        </View>
    );
}

