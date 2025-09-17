//file used for rendering actual game play
import { Canvas, Path } from '@shopify/react-native-skia';
import React from 'react';
import { Dimensions, View } from 'react-native';

export default function SkiaTest() {
  const { width, height} = Dimensions.get('window');
  const canvasSize = 300;
  ;
  
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <Canvas style={{ width: 250, height: 400, borderWidth: 2, borderColor: 'red', transform: [{translateY: -200}, {translateX: 70}]}}>
          <Path
            path="M 120 120 L 180 120 L 180 180 L 120 180 Z"
            color="#8ED6FF"
            style="fill"
            strokeWidth={2}
          />
        </Canvas>
      </View>
    );
  }

