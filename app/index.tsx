//file used for rendering actual game play
//THIS IS <NOT> THE ORIGINAL index.tsx CHANGE THIS BACK TO gamePlay.tsx ONCE FINISHED RENDERING GAME. CHANGE
//login.tsx BACK TO index.tsx
import { Canvas, Image, Mask, Path, useImage } from '@shopify/react-native-skia';
import React from 'react';
import { Dimensions, View } from 'react-native';

export default function renderSkiaGraphics() {
  const { width, height} = Dimensions.get('window');
  const canvasSize = 300;
  const texture = useImage(require('./images/bricks.png'))
  //BELOW IS COMMENTED OUT UNTIL GAME DESIGN IS CREATED
  /* 
  const { username, dailyInfoOne, dailyInfoTwo, dailyInfoThree} = useLocalSearchParams();
  const parsedToSendOne = dailyInfoOne && typeof dailyInfoOne == "string" ? JSON.parse(dailyInfoOne) : [];
  const parsedToSendTwo = dailyInfoTwo && typeof dailyInfoTwo == "string" ? JSON.parse(dailyInfoTwo) : [];
  const parsedToSendThree = dailyInfoThree && typeof dailyInfoThree == "string" ? JSON.parse(dailyInfoThree) : [];
  
  const changeRegion = () => {
    
  }
  */
  
  return (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Canvas style={{ width: 250, height: 400 }}>
      {texture && (
        <Mask mask={
          <Path path="M 220 210 L 220 145 L 140 90 L 0 177.5 L 140 255 L 220 210" />
        }>
          <Image image={texture} width={250} height={400} />
        </Mask>
      )}
    </Canvas>
  </View>
);
}

