import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useWalletStore } from '@/store/walletStore';
import { CategoryIcon } from '@/components/ui/CategoryIcon';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { CATEGORIES } from '@/constants/categories';
import { Colors } from '@/constants/colors';
import { TransactionType, TransactionCategory } from '@/types';

export default function AddTransactionScreen() {
  const { addTransaction } = useWalletStore();
  const [type, setType] = useState<TransactionType>('expense');
  const [amount, setAmount] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [category, setCategory] = useState<TransactionCategory>('other');

  const handleSave = () => {
    if (!amount || !title) {
      Alert.alert('Error', 'Please fill in all required fields.');
      return;
    }

    const numericAmount = parseFloat(amount);
    if (isNaN(numericAmount) || numericAmount <= 0) {
      Alert.alert('Error', 'Please enter a valid amount.');
      return;
    }

    addTransaction({
      title: title.trim(),
      amount: numericAmount,
      type,
      category,
      date: new Date().toISOString(),
      description: description.trim() || undefined,
    });

    Alert.alert('Success', 'Transaction added successfully!', [
      { text: 'OK', onPress: () => router.back() }
    ]);
  };

  const filteredCategories = CATEGORIES.filter(cat => {
    if (type === 'income') {
      return ['salary', 'freelance', 'business', 'investment', 'gift', 'other'].includes(cat.id);
    }
    return !['salary', 'freelance', 'business', 'investment'].includes(cat.id);
  });

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()}>
            <Ionicons name="close" size={24} color={Colors.text} />
          </TouchableOpacity>
          <Text style={styles.title}>Add Transaction</Text>
          <View style={{ width: 24 }} />
        </View>

        {/* Type Selector */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Transaction Type</Text>
          <View style={styles.typeContainer}>
            <TouchableOpacity
              style={[
                styles.typeButton,
                type === 'income' && styles.typeButtonActive,
                { borderColor: Colors.income },
              ]}
              onPress={() => setType('income')}
            >
              <Ionicons
                name="trending-up"
                size={20}
                color={type === 'income' ? Colors.income : Colors.textSecondary}
              />
              <Text
                style={[
                  styles.typeButtonText,
                  { color: type === 'income' ? Colors.income : Colors.textSecondary },
                ]}
              >
                Income
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.typeButton,
                type === 'expense' && styles.typeButtonActive,
                { borderColor: Colors.expense },
              ]}
              onPress={() => setType('expense')}
            >
              <Ionicons
                name="trending-down"
                size={20}
                color={type === 'expense' ? Colors.expense : Colors.textSecondary}
              />
              <Text
                style={[
                  styles.typeButtonText,
                  { color: type === 'expense' ? Colors.expense : Colors.textSecondary },
                ]}
              >
                Expense
              </Text>
            </TouchableOpacity>
          </View>
        </Card>

        {/* Amount Input */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Amount *</Text>
          <View style={styles.amountContainer}>
            <Text style={styles.currencySymbol}>$</Text>
            <TextInput
              style={styles.amountInput}
              value={amount}
              onChangeText={setAmount}
              placeholder="0.00"
              placeholderTextColor={Colors.textTertiary}
              keyboardType="numeric"
              autoFocus={true}
            />
          </View>
        </Card>

        {/* Title Input */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Title *</Text>
          <TextInput
            style={styles.textInput}
            value={title}
            onChangeText={setTitle}
            placeholder="Enter transaction title"
            placeholderTextColor={Colors.textTertiary}
          />
        </Card>

        {/* Category Selector */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Category</Text>
          <View style={styles.categoriesGrid}>
            {filteredCategories.map((cat) => (
              <TouchableOpacity
                key={cat.id}
                style={[
                  styles.categoryItem,
                  category === cat.id && styles.categoryItemActive,
                ]}
                onPress={() => setCategory(cat.id)}
              >
                <CategoryIcon
                  category={cat.id}
                  size={20}
                  showBackground={category === cat.id}
                />
                <Text
                  style={[
                    styles.categoryText,
                    category === cat.id && styles.categoryTextActive,
                  ]}
                >
                  {cat.name}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </Card>

        {/* Description Input */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Description (Optional)</Text>
          <TextInput
            style={[styles.textInput, styles.descriptionInput]}
            value={description}
            onChangeText={setDescription}
            placeholder="Add a note..."
            placeholderTextColor={Colors.textTertiary}
            multiline
            numberOfLines={3}
          />
        </Card>

        {/* Save Button */}
        <View style={styles.buttonContainer}>
          <Button
            title="Save Transaction"
            onPress={handleSave}
            variant="primary"
            size="large"
            fullWidth
          />
        </View>

        {/* Bottom Spacing */}
        <View style={styles.bottomSpacing} />
      </ScrollView>
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
  section: {
    margin: 16,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 12,
  },
  typeContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  typeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 20,
    borderRadius: 12,
    borderWidth: 2,
    backgroundColor: Colors.surface,
  },
  typeButtonActive: {
    backgroundColor: Colors.backgroundSecondary,
  },
  typeButtonText: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  amountContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: 12,
    paddingHorizontal: 16,
  },
  currencySymbol: {
    fontSize: 24,
    fontWeight: '600',
    color: Colors.text,
    marginRight: 8,
  },
  amountInput: {
    flex: 1,
    fontSize: 24,
    fontWeight: '600',
    color: Colors.text,
    paddingVertical: 16,
  },
  textInput: {
    backgroundColor: Colors.backgroundSecondary,
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 16,
    color: Colors.text,
  },
  descriptionInput: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  categoryItem: {
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: Colors.backgroundSecondary,
    minWidth: '30%',
  },
  categoryItemActive: {
    backgroundColor: Colors.primary + '20',
    borderWidth: 2,
    borderColor: Colors.primary,
  },
  categoryText: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 4,
    textAlign: 'center',
  },
  categoryTextActive: {
    color: Colors.primary,
    fontWeight: '600',
  },
  buttonContainer: {
    paddingHorizontal: 16,
    paddingTop: 8,
  },
  bottomSpacing: {
    height: 40,
  },
});