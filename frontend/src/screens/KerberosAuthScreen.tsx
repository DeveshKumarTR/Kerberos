import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Title, Paragraph, Button, ProgressBar, List, Chip } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';
import { KerberosService } from '../services/KerberosService';

interface KerberosAuthScreenProps {
  navigation: any;
}

const KerberosAuthScreen: React.FC<KerberosAuthScreenProps> = ({ navigation }) => {
  const [authStep, setAuthStep] = useState(0);
  const [authStatus, setAuthStatus] = useState<string[]>([]);
  const [isAuthenticating, setIsAuthenticating] = useState(false);

  const authSteps = [
    'Connecting to Authentication Server (AS)',
    'Validating credentials with Claude AI',
    'Requesting Ticket Granting Ticket (TGT)',
    'Connecting to Ticket Granting Server (TGS)',
    'Requesting Service Ticket',
    'Accessing protected resources'
  ];

  const startAuthentication = async () => {
    setIsAuthenticating(true);
    setAuthStep(0);
    setAuthStatus([]);

    for (let i = 0; i < authSteps.length; i++) {
      setAuthStep(i + 1);
      setAuthStatus(prev => [...prev, `✅ ${authSteps[i]}`]);
      
      // Simulate authentication delay
      await new Promise(resolve => setTimeout(resolve, 1500));
    }

    setIsAuthenticating(false);
  };

  const getProgressValue = () => {
    return authStep / authSteps.length;
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <Card style={styles.card}>
          <Card.Content>
            <Title>🐕‍🦺 Kerberos Three-Head Authentication</Title>
            <Paragraph style={styles.description}>
              Experience the full Kerberos authentication flow with AI-enhanced security
            </Paragraph>
            
            <ProgressBar 
              progress={getProgressValue()} 
              color="#1976d2" 
              style={styles.progressBar}
            />
            
            <Paragraph style={styles.stepText}>
              Step {authStep} of {authSteps.length}
            </Paragraph>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>Authentication Process</Title>
            {authStatus.map((status, index) => (
              <List.Item
                key={index}
                title={status}
                left={() => <List.Icon icon="check" color="green" />}
              />
            ))}
            
            {isAuthenticating && authStep < authSteps.length && (
              <List.Item
                title={`🔄 ${authSteps[authStep]}`}
                left={() => <List.Icon icon="loading" />}
              />
            )}
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>🤖 Claude AI Integration</Title>
            <View style={styles.chipContainer}>
              <Chip icon="brain">Threat Detection</Chip>
              <Chip icon="shield-check">Behavior Analysis</Chip>
              <Chip icon="eye">Anomaly Detection</Chip>
            </View>
            <Paragraph style={styles.aiDescription}>
              Claude AI continuously monitors authentication patterns and enhances security
            </Paragraph>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>📊 Pinecone Vector Database</Title>
            <Paragraph>
              Secure storage and retrieval of authentication vectors and user patterns
            </Paragraph>
            <List.Item
              title="Vector Embeddings"
              description="User behavior patterns"
              left={() => <List.Icon icon="vector-triangle" />}
            />
            <List.Item
              title="Similarity Search"
              description="Anomaly detection"
              left={() => <List.Icon icon="magnify" />}
            />
          </Card.Content>
        </Card>

        <Button
          mode="contained"
          onPress={startAuthentication}
          style={styles.button}
          disabled={isAuthenticating}
        >
          {isAuthenticating ? 'Authenticating...' : 'Start Authentication Flow'}
        </Button>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 16,
    elevation: 4,
  },
  description: {
    marginBottom: 16,
    color: '#666',
  },
  progressBar: {
    marginVertical: 16,
    height: 8,
  },
  stepText: {
    textAlign: 'center',
    fontWeight: 'bold',
    color: '#1976d2',
  },
  chipContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 12,
  },
  aiDescription: {
    color: '#666',
    fontSize: 14,
  },
  button: {
    margin: 16,
    paddingVertical: 8,
  },
});

export default KerberosAuthScreen;
