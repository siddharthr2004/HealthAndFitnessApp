//file used for rendering actual game play
//THIS IS <NOT> THE ORIGINAL index.tsx CHANGE THIS BACK TO gamePlay.tsx ONCE FINISHED RENDERING GAME. CHANGE
//login.tsx BACK TO index.tsx
import { Canvas, Image, Mask, Path, useImage } from '@shopify/react-native-skia';
import { useLocalSearchParams } from 'expo-router';
import { Dimensions, View } from 'react-native';

export default function renderSkiaGraphics() {
  const { width, height} = Dimensions.get('window');
  const screenWidth = width;
  const screenHeight = height;
  let house = useImage(require('./images/houseLevelOne.png'));
  //retrieve username, and daily info values
  const { username, dailyInfoOne, dailyInfoTwo, dailyInfoThree} = useLocalSearchParams();
  //parses out the values, converts the string json into js objects
  const parsedToSendOne = dailyInfoOne && typeof dailyInfoOne == "string" ? JSON.parse(dailyInfoOne) : [];
  const parsedToSendTwo = dailyInfoTwo && typeof dailyInfoTwo == "string" ? JSON.parse(dailyInfoTwo) : [];
  const parsedToSendThree = dailyInfoThree && typeof dailyInfoThree == "string" ? JSON.parse(dailyInfoThree) : [];
  //TEST
  console.log(parsedToSendOne);
  console.log(parsedToSendTwo);
  console.log(parsedToSendThree);
  //iterate through vals
  for (let i=0; i<parsedToSendOne.length; ++i) {
    console.log("came here");
    if (parsedToSendOne[i] == "hoursProductiveDeviation") {
      house = useImage(require('./images/houseLevelTwo.png'));
    }
  }
 
  return (
      <View style = {{flex: 1, justifyContent: 'center', alignItems: 'center'}}>
        <Canvas style={{width: screenWidth, height: screenHeight}}>
          {house && 
            <Mask mask={
              <Path path={`M 0 0 L ${screenWidth} 0 L ${screenHeight} ${screenWidth} L 0 ${screenHeight}`}/>
            }>
              <Image image={house} width={screenWidth} height={screenHeight}></Image>
            </Mask> 
          }
        </Canvas>
      </View>
  )
}

