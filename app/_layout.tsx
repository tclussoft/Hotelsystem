import React from 'react';
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';
import { Colors } from '@/constants/colors';

export default function RootLayout() {
  return (
    <>
      <StatusBar style="dark" backgroundColor={Colors.background} />
      <Stack
        screenOptions={{
          headerShown: false,
          contentStyle: { backgroundColor: Colors.background },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen 
          name="transaction/add" 
          options={{ 
            presentation: 'modal',
            headerShown: true,
            headerTitle: 'Add Transaction',
            headerStyle: { backgroundColor: Colors.surface },
            headerTitleStyle: { color: Colors.text, fontWeight: '600' },
          }} 
        />
        <Stack.Screen 
          name="transaction/[id]" 
          options={{ 
            headerShown: true,
            headerTitle: 'Transaction Details',
            headerStyle: { backgroundColor: Colors.surface },
            headerTitleStyle: { color: Colors.text, fontWeight: '600' },
          }} 
        />
        <Stack.Screen 
          name="modal" 
          options={{ 
            presentation: 'modal',
            headerShown: true,
            headerTitle: 'Information',
            headerStyle: { backgroundColor: Colors.surface },
            headerTitleStyle: { color: Colors.text, fontWeight: '600' },
          }} 
        />
      </Stack>
    </>
  );
}