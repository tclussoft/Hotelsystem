import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  FlatList,
} from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useWalletStore } from '@/store/walletStore';
import { BalanceCard } from '@/components/dashboard/BalanceCard';
import { TransactionItem } from '@/components/transactions/TransactionItem';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Colors } from '@/constants/colors';

export default function DashboardScreen() {
  const { transactions, getAnalytics } = useWalletStore();
  const analytics = getAnalytics();
  const recentTransactions = transactions.slice(0, 5);

  const handleAddTransaction = () => {
    router.push('/transaction/add');
  };

  const handleViewAllTransactions = () => {
    router.push('/transactions');
  };

  const handleTransactionPress = (id: string) => {
    router.push(`/transaction/${id}`);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Good morning!</Text>
            <Text style={styles.subtitle}>Here's your financial overview</Text>
          </View>
          <TouchableOpacity
            style={styles.profileButton}
            onPress={() => router.push('/modal')}
          >
            <Ionicons name="person-circle-outline" size={32} color={Colors.primary} />
          </TouchableOpacity>
        </View>

        {/* Balance Card */}
        <BalanceCard
          balance={analytics.balance}
          totalIncome={analytics.totalIncome}
          totalExpenses={analytics.totalExpenses}
        />

        {/* Quick Actions */}
        <Card style={styles.actionsCard}>
          <Text style={styles.sectionTitle}>Quick Actions</Text>
          <View style={styles.actionsContainer}>
            <Button
              title="Add Income"
              onPress={handleAddTransaction}
              variant="primary"
              style={styles.actionButton}
            />
            <Button
              title="Add Expense"
              onPress={handleAddTransaction}
              variant="outline"
              style={styles.actionButton}
            />
          </View>
        </Card>

        {/* Recent Transactions */}
        <Card style={styles.transactionsCard}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Recent Transactions</Text>
            <TouchableOpacity onPress={handleViewAllTransactions}>
              <Text style={styles.viewAllText}>View All</Text>
            </TouchableOpacity>
          </View>

          {recentTransactions.length > 0 ? (
            <View style={styles.transactionsList}>
              {recentTransactions.map((transaction) => (
                <TransactionItem
                  key={transaction.id}
                  transaction={transaction}
                  onPress={() => handleTransactionPress(transaction.id)}
                />
              ))}
            </View>
          ) : (
            <View style={styles.emptyState}>
              <Ionicons name="receipt-outline" size={48} color={Colors.textTertiary} />
              <Text style={styles.emptyStateText}>No transactions yet</Text>
              <Text style={styles.emptyStateSubtext}>
                Add your first transaction to get started
              </Text>
            </View>
          )}
        </Card>

        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>

      {/* Floating Add Button */}
      <TouchableOpacity style={styles.fab} onPress={handleAddTransaction}>
        <Ionicons name="add" size={28} color={Colors.textInverse} />
      </TouchableOpacity>
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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 10,
  },
  greeting: {
    fontSize: 24,
    fontWeight: '700',
    color: Colors.text,
  },
  subtitle: {
    fontSize: 16,
    color: Colors.textSecondary,
    marginTop: 4,
  },
  profileButton: {
    padding: 4,
  },
  actionsCard: {
    margin: 16,
    marginTop: 20,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 16,
  },
  actionsContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  actionButton: {
    flex: 1,
  },
  transactionsCard: {
    margin: 16,
    padding: 0,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  viewAllText: {
    fontSize: 14,
    color: Colors.primary,
    fontWeight: '500',
  },
  transactionsList: {
    marginTop: 8,
  },
  emptyState: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingHorizontal: 16,
  },
  emptyStateText: {
    fontSize: 16,
    fontWeight: '500',
    color: Colors.textSecondary,
    marginTop: 12,
  },
  emptyStateSubtext: {
    fontSize: 14,
    color: Colors.textTertiary,
    marginTop: 4,
    textAlign: 'center',
  },
  bottomSpacing: {
    height: 100,
  },
  fab: {
    position: 'absolute',
    bottom: 30,
    right: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: Colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 4,
    },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
});