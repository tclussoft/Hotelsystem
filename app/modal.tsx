import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Card } from '@/components/ui/Card';
import { Colors } from '@/constants/colors';

export default function ModalScreen() {
  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Ionicons name="close" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.title}>About</Text>
        <View style={{ width: 24 }} />
      </View>

      {/* Content */}
      <View style={styles.content}>
        <Card style={styles.infoCard}>
          <View style={styles.logoContainer}>
            <Ionicons name="wallet" size={64} color={Colors.primary} />
          </View>
          
          <Text style={styles.appName}>Wallet Tracker</Text>
          <Text style={styles.version}>Version 1.0.0</Text>
          
          <Text style={styles.description}>
            A beautiful and intuitive expense tracking app designed to help you manage your finances with ease. 
            Track your income and expenses, set budgets, and gain insights into your spending habits.
          </Text>
          
          <View style={styles.features}>
            <Text style={styles.featuresTitle}>Features:</Text>
            <Text style={styles.feature}>• Beautiful iOS-inspired design</Text>
            <Text style={styles.feature}>• Track income and expenses</Text>
            <Text style={styles.feature}>• Categorize transactions</Text>
            <Text style={styles.feature}>• Visual analytics and insights</Text>
            <Text style={styles.feature}>• Data persistence</Text>
          </View>
        </Card>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  infoCard: {
    alignItems: 'center',
    paddingVertical: 32,
  },
  logoContainer: {
    marginBottom: 24,
  },
  appName: {
    fontSize: 28,
    fontWeight: '700',
    color: Colors.text,
    marginBottom: 8,
  },
  version: {
    fontSize: 16,
    color: Colors.textSecondary,
    marginBottom: 24,
  },
  description: {
    fontSize: 16,
    color: Colors.textSecondary,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 32,
  },
  features: {
    alignSelf: 'stretch',
  },
  featuresTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 12,
  },
  feature: {
    fontSize: 16,
    color: Colors.textSecondary,
    marginBottom: 8,
    lineHeight: 22,
  },
});