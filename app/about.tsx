import { Text, View, StyleSheet} from 'react-native'

export default function AboutScreen() {
    return (
        <View style={styles.container}>
            <text style={styles.text}>About screen</text>
        </View>
    );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#25292e',
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    color: '#fff',
  },
});