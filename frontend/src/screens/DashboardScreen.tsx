import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Title, Paragraph, Button, List, Divider } from 'react-native-paper';
import { SafeAreaView } from 'react-native-safe-area-context';

interface DashboardScreenProps {
  navigation: any;
  route: any;
}

const DashboardScreen: React.FC<DashboardScreenProps> = ({ navigation, route }) => {
  const { user } = route.params || {};

  const handleKerberosAuth = () => {
    navigation.navigate('KerberosAuth');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView>
        <Card style={styles.welcomeCard}>
          <Card.Content>
            <Title>Welcome, {user?.username || 'User'}!</Title>
            <Paragraph>Kerberos Protocol Dashboard</Paragraph>
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>🛡️ Security Status</Title>
            <List.Item
              title="Authentication Status"
              description="Active"
              left={() => <List.Icon icon="check-circle" color="green" />}
            />
            <List.Item
              title="Token Validity"
              description="Valid for 8 hours"
              left={() => <List.Icon icon="clock" color="blue" />}
            />
            <List.Item
              title="Security Level"
              description="High"
              left={() => <List.Icon icon="shield-check" color="green" />}
            />
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>🐕‍🦺 Three-Headed Authentication</Title>
            <Paragraph style={styles.description}>
              Experience the power of Kerberos protocol with our three-layered security approach:
            </Paragraph>
            <List.Item
              title="Authentication Server (AS)"
              description="Initial identity verification"
              left={() => <List.Icon icon="account-check" />}
            />
            <List.Item
              title="Ticket Granting Server (TGS)"
              description="Service ticket management"
              left={() => <List.Icon icon="ticket" />}
            />
            <List.Item
              title="Service Server (SS)"
              description="Resource access control"
              left={() => <List.Icon icon="server" />}
            />
          </Card.Content>
        </Card>

        <Card style={styles.card}>
          <Card.Content>
            <Title>🤖 AI Integration</Title>
            <Paragraph>
              Claude AI enhances security with intelligent threat detection and adaptive authentication.
            </Paragraph>
            <Button
              mode="outlined"
              onPress={handleKerberosAuth}
              style={styles.button}
            >
              Start Kerberos Authentication
            </Button>
          </Card.Content>
        </Card>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  welcomeCard: {
    margin: 16,
    elevation: 4,
  },
  card: {
    margin: 16,
    marginTop: 8,
    elevation: 4,
  },
  description: {
    marginBottom: 16,
    color: '#666',
  },
  button: {
    marginTop: 16,
  },
});

export default DashboardScreen;
