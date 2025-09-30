//file used for rendering actual game play
//THIS IS <NOT> THE ORIGINAL index.tsx CHANGE THIS BACK TO gamePlay.tsx ONCE FINISHED RENDERING GAME. CHANGE
//login.tsx BACK TO index.tsx
import { useFont, useImage } from '@shopify/react-native-skia';
import { Dimensions } from 'react-native';

export default function renderSkiaGraphics() {
  const { width, height} = Dimensions.get('window');
  const canvasSize = 300;
  const texture = useImage(require('./images/bricks.png'));
  const windows = useImage(require('./images/mirror.png'));
  const door = useImage(require('./images/door.png'))
  //font to view positioning rendering
  const font = useFont(require('./images/Roboto.ttf'), 12);
  //Below will be used to check if image rendering directly works fine here
  const houseLevelOne = useImage(require(',.images/houseLevelOne'));
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
    {/*Commented out this section for now to test rendering of image 
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Canvas style={{ width: 250, height: 400, borderWidth: 1, transform: [{translateY: -200}, {translateX: 70}]}}>
      {texture && (
        <Mask mask={
          <Path path="M 286 364 L 286 188.5 L 182 117 L 0 230.75 L 182 331.5 L 286 273" />
        }>
          <Image image={texture} width={250} height={400} />
        </Mask>
      )}
      
      {windows && (
        <Mask mask={
          <Path path="M 180 275 L 155 275 L 155 250 L 180 250 L 180 275"/>
        }>
          <Image image={windows} width={250} height={400} />
          <Path path = "M 167.5 275 L 167.5 250" color="black" style="stroke" strokeWidth={2}/>
          <Path path = "M 155 262.5 L 180 262.5" color="black" style="stroke" strokeWidth={2}/>
        </Mask>
      )}
      
      {windows && (
        <Mask mask={
          <Path path="M 180 205 L 180 180 L 155 180 L 155 205 L 180 205"/>
        }>
          <Image image={windows} width={250} height={400} />
          <Path path="M 167.5 180 L 167.5 205" color="black" style="stroke" strokeWidth={2}/>
          <Path path="M 155 192.5 L 180 192.5" color="black" style="stroke" strokeWidth={2}/>
        </Mask>
      )}
      
      {door && (
        <Mask mask={
          <Path path="M 235 245 L 235 220 L 195 220 L 195 245 L 235 245" />
        }>
          <Image image={door} x={195} y={220} width={40} height={25} />
        </Mask>
      )}
      
      {door && (
        <Mask mask={
          <Path path="M 235 245 L 235 220 L 195 220 L 195 245 L 235 245" />
        }>
          <Image image={door} x={195} y={220} width={40} height={25} />
        </Mask>
      )}
      
      <Text x={100} y={10} text="1" color="red" font={font}/>
      <Text x={200} y={10} text="2" color="red" font={font}/>
      <Text x={0} y={100} text="01" color="red" font={font}/>
      <Text x={0} y={200} text="02" color="red" font={font}/>
      <Text x={0} y={300} text="03" color="red" font={font}/>
      <Text x={0} y={400} text="04" color="red" font={font}/>

    </Canvas>
  </View>
);
    */}
      
    )
}

