import { useLocalSearchParams, useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Button, Text, TextInput, View } from 'react-native';

export default function AboutScreen() {
    const router = useRouter();
    const [message, setMessage] = useState('');
    const { username } = useLocalSearchParams();
    const [calsEaten, setCalsEaten] = useState('');
    const [socialMediaHrs, setSocialMediaHrs] = useState('');
    const [calsBurned, setCalsBurned] = useState('')
    const [waterDrank, setWaterDrank] = useState('')
    const [hrsProductive, setHrsProductive] = useState('');
    const vals = {
      "username": username,
      "calsEaten": calsEaten, 
      "socialMediaHrs": socialMediaHrs,
      "calsBurned": calsBurned,
      "waterDrank": waterDrank,
      "hrsProductive": hrsProductive
    };
    const run = () => {
        fetch('http://localhost:5001/firstInfo', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(vals),
      })
      .then(response => response.json())
      .then(data => {
        if (data == 0) {
          setMessage("Your data was not able to be inputted. Sorry for the inconvinience");
        } else {
          setMessage("");
          router.back()
        }
      })
      .catch(error => {
        console.log(error);
      })
    };
    return (
        <View style={{padding:20}}>
          <Text>Enter calories eaten:</Text>
          <TextInput value={calsEaten} onChangeText={setCalsEaten} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter hours on social media spent:</Text>
          <TextInput value={socialMediaHrs} onChangeText={setSocialMediaHrs} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter calories burned:</Text>
          <TextInput value={calsBurned} onChangeText={setCalsBurned} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter total water drank:</Text>
          <TextInput value={waterDrank} onChangeText={setWaterDrank} style={{borderWidth: 1, marginBottom: 10}}/>
          <Text>Enter total hours productive:</Text>
          <TextInput value={hrsProductive} onChangeText={setHrsProductive} style={{borderWidth: 1, marginBottom: 10}}/>
          <Button title="Run" onPress={run} />
        </View>
    );
}

