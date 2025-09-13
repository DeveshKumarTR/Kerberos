import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { TextInput, Button, Card, Title, Paragraph, ActivityIndicator } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { KerberosService } from '../services/KerberosService';

interface LoginScreenProps {
  navigation: any;
}

const LoginScreen: React.FC<LoginScreenProps> = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter both username and password');
      return;
    }

    setLoading(true);
    try {
      const result = await KerberosService.authenticate(username, password);
      if (result.success) {
        navigation.navigate('Dashboard', { user: result.user });
      } else {
        Alert.alert('Authentication Failed', result.message);
      }
    } catch (error) {
      Alert.alert('Error', 'An error occurred during authentication');
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>🐕‍🦺 Kerberos Protocol</Title>
          <Paragraph style={styles.subtitle}>
            Secure Three-Headed Authentication System
          </Paragraph>
          
          <TextInput
            label="Username"
            value={username}
            onChangeText={setUsername}
            mode="outlined"
            style={styles.input}
            autoCapitalize="none"
          />
          
          <TextInput
            label="Password"
            value={password}
            onChangeText={setPassword}
            mode="outlined"
            secureTextEntry
            style={styles.input}
          />
          
          <Button
            mode="contained"
            onPress={handleLogin}
            style={styles.button}
            disabled={loading}
          >
            {loading ? <ActivityIndicator color="white" /> : 'Login'}
          </Button>
        </Card.Content>
      </Card>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  card: {
    elevation: 8,
    borderRadius: 12,
  },
  title: {
    textAlign: 'center',
    fontSize: 24,
    marginBottom: 8,
    color: '#1976d2',
  },
  subtitle: {
    textAlign: 'center',
    marginBottom: 24,
    color: '#666',
  },
  input: {
    marginBottom: 16,
  },
  button: {
    marginTop: 8,
    paddingVertical: 8,
  },
});

export default LoginScreen;
