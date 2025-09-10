import { useRouter } from 'expo-router';
import React, { useState } from 'react';
import { Button, Text, TextInput, View } from 'react-native';

export default function loginInfo() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [firstUsername, setFirstUsername] = useState('');
    const [firstPassword, setFirstPassword] = useState('');
    const[message, setMessage] = useState('');
    const vals = {
        "username": username,
        "password": password
    }
    const firstVals = {
        "username": firstUsername,
        "password": firstPassword
    }
    const router = useRouter();
    const runRegister = () => {
        fetch('http://localhost:5001/register', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify(firstVals)
        })
        .then(response => response.json())
        .then(data => {
            if (data == 0) {
                setMessage("This account already exists. Enter another username");
            } else {
                setMessage("");
                router.push({
                    //Change this back to a singular / once you start to run, two slashes used to placate error
                    pathname: '//firstInfo',
                    params: {username}
                });
            }
        })
        .catch(err => {
            console.log(err);
        })
    }
    const run = () => {
        fetch('http://localhost:5001/loginInfo', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify(vals)
        })
        .then(response => response.json())
        .then(data => {
            if (data == 0) {
                setMessage("Login credentials were incorrect");
            } else {
                setMessage("");
                router.push({
                    //Change this back to a singular / once you start to run, two slashes used to placate error
                    pathname: "//dailyInfo",
                    params: {username}
                });
            }
        })
        .catch(error => {
            console.log(error);
        })
    }
    return (
        <><View style={{padding:20}}>
                <Text>Login:</Text>
                <Text>Enter username:</Text>
                <TextInput value={username} onChangeText={setUsername} style={{borderWidth: 1, marginBottom: 10}}/>
                <Text>Enter password:</Text>
                <TextInput value={password} onChangeText={setPassword} style={{borderWidth: 1, marginBottom: 10}}/>
                <Button title = "login" onPress={run}/>
            </View>
            
            <View style={{flexDirection: 'row', alignItems: 'center'}} >
                <Text>Register:</Text>
                <Text>Enter username:</Text>
                <TextInput value={firstUsername} onChangeText={setFirstUsername} style={{borderWidth: 1, marginBottom: 10}}/>
                <Text>Enter Password:</Text>
                <TextInput value={firstPassword} onChangeText={setFirstPassword} style={{borderWidth: 1, marginBottom: 10}}/>
                <Button title = "register now!" onPress={runRegister}/>
                <Text>{message}</Text>
            </View></>
    );
}
