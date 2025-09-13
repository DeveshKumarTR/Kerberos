import { DefaultTheme } from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#1976d2',
    accent: '#03dac4',
    background: '#f5f5f5',
    surface: '#ffffff',
    text: '#000000',
    placeholder: '#666666',
    backdrop: 'rgba(0, 0, 0, 0.5)',
    onSurface: '#000000',
    notification: '#f50057',
    error: '#b00020',
    success: '#4caf50',
    warning: '#ff9800',
    info: '#2196f3',
  },
  fonts: {
    ...DefaultTheme.fonts,
    regular: {
      fontFamily: 'System',
      fontWeight: '400' as '400',
    },
    medium: {
      fontFamily: 'System',
      fontWeight: '500' as '500',
    },
    light: {
      fontFamily: 'System',
      fontWeight: '300' as '300',
    },
    thin: {
      fontFamily: 'System',
      fontWeight: '100' as '100',
    },
  },
  roundness: 8,
};
