import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { Card } from '@/components/ui/Card';
import { formatAmount } from '@/utils/formatters';
import { Colors } from '@/constants/colors';

interface BalanceCardProps {
  balance: number;
  totalIncome: number;
  totalExpenses: number;
}

export const BalanceCard: React.FC<BalanceCardProps> = ({
  balance,
  totalIncome,
  totalExpenses,
}) => {
  return (
    <Card padding={0} style={styles.container}>
      <LinearGradient
        colors={[Colors.primary, Colors.primaryDark]}
        style={styles.gradient}
        start={{ x: 0, y: 0 }}
        end={{ x: 1, y: 1 }}
      >
        <View style={styles.content}>
          <Text style={styles.label}>Total Balance</Text>
          <Text style={styles.balance}>
            {formatAmount(balance, true)}
          </Text>
          
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statLabel}>Income</Text>
              <Text style={[styles.statValue, { color: Colors.successLight }]}>
                +{formatAmount(totalIncome)}
              </Text>
            </View>
            
            <View style={styles.statItem}>
              <Text style={styles.statLabel}>Expenses</Text>
              <Text style={[styles.statValue, { color: Colors.errorLight }]}>
                -{formatAmount(totalExpenses)}
              </Text>
            </View>
          </View>
        </View>
      </LinearGradient>
    </Card>
  );
};

const styles = StyleSheet.create({
  container: {
    marginHorizontal: 16,
    marginTop: 20,
    overflow: 'hidden',
  },
  gradient: {
    padding: 24,
    borderRadius: 16,
  },
  content: {
    alignItems: 'center',
  },
  label: {
    fontSize: 16,
    color: Colors.textInverse,
    opacity: 0.8,
    marginBottom: 8,
  },
  balance: {
    fontSize: 36,
    fontWeight: '700',
    color: Colors.textInverse,
    marginBottom: 24,
  },
  statsContainer: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 14,
    color: Colors.textInverse,
    opacity: 0.7,
    marginBottom: 4,
  },
  statValue: {
    fontSize: 18,
    fontWeight: '600',
  },
});