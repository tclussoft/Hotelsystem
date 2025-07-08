import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Transaction } from '@/types';
import { CategoryIcon } from '@/components/ui/CategoryIcon';
import { formatAmount, formatDate } from '@/utils/formatters';
import { Colors } from '@/constants/colors';

interface TransactionItemProps {
  transaction: Transaction;
  onPress?: () => void;
  showDate?: boolean;
}

export const TransactionItem: React.FC<TransactionItemProps> = ({
  transaction,
  onPress,
  showDate = true,
}) => {
  const isIncome = transaction.type === 'income';
  const amountColor = isIncome ? Colors.income : Colors.expense;

  return (
    <TouchableOpacity
      style={styles.container}
      onPress={onPress}
      activeOpacity={0.7}
      disabled={!onPress}
    >
      <CategoryIcon category={transaction.category} size={20} />
      
      <View style={styles.content}>
        <View style={styles.header}>
          <Text style={styles.title} numberOfLines={1}>
            {transaction.title}
          </Text>
          <Text style={[styles.amount, { color: amountColor }]}>
            {isIncome ? '+' : '-'}{formatAmount(transaction.amount)}
          </Text>
        </View>
        
        <View style={styles.footer}>
          {transaction.description && (
            <Text style={styles.description} numberOfLines={1}>
              {transaction.description}
            </Text>
          )}
          {showDate && (
            <Text style={styles.date}>
              {formatDate(transaction.date)}
            </Text>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.borderLight,
  },
  content: {
    flex: 1,
    marginLeft: 12,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 4,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
    flex: 1,
    marginRight: 8,
  },
  amount: {
    fontSize: 16,
    fontWeight: '700',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  description: {
    fontSize: 14,
    color: Colors.textSecondary,
    flex: 1,
    marginRight: 8,
  },
  date: {
    fontSize: 12,
    color: Colors.textTertiary,
  },
});