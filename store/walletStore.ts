import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { WalletState, Transaction, Budget, AnalyticsData } from '@/types';
import { 
  calculateBalance, 
  calculateTotalByType, 
  calculateCategorySpending, 
  getMonthlyTrends 
} from '@/utils/calculations';

// Mock data for initial state
const mockTransactions: Transaction[] = [
  {
    id: '1',
    title: 'Coffee Shop',
    amount: 4.50,
    type: 'expense',
    category: 'food',
    date: new Date().toISOString(),
    description: 'Morning coffee',
    location: 'Starbucks',
  },
  {
    id: '2',
    title: 'Grocery Store',
    amount: 85.30,
    type: 'expense',
    category: 'groceries',
    date: new Date(Date.now() - 86400000).toISOString(), // Yesterday
    description: 'Weekly groceries',
  },
  {
    id: '3',
    title: 'Salary',
    amount: 3500.00,
    type: 'income',
    category: 'salary',
    date: new Date(Date.now() - 86400000 * 2).toISOString(), // 2 days ago
    description: 'Monthly salary payment',
  },
  {
    id: '4',
    title: 'Uber Ride',
    amount: 12.75,
    type: 'expense',
    category: 'transport',
    date: new Date(Date.now() - 86400000 * 3).toISOString(), // 3 days ago
    description: 'Ride to downtown',
  },
  {
    id: '5',
    title: 'Netflix Subscription',
    amount: 15.99,
    type: 'expense',
    category: 'entertainment',
    date: new Date(Date.now() - 86400000 * 5).toISOString(), // 5 days ago
    description: 'Monthly subscription',
  },
];

const mockBudgets: Budget[] = [
  {
    id: '1',
    category: 'food',
    limit: 200,
    spent: 45.50,
    period: 'monthly',
  },
  {
    id: '2',
    category: 'transport',
    limit: 100,
    spent: 67.25,
    period: 'monthly',
  },
  {
    id: '3',
    category: 'entertainment',
    limit: 50,
    spent: 35.99,
    period: 'monthly',
  },
];

export const useWalletStore = create<WalletState>()(
  persist(
    (set, get) => ({
      transactions: mockTransactions,
      budgets: mockBudgets,
      balance: calculateBalance(mockTransactions),

      addTransaction: (transaction) => {
        const newTransaction: Transaction = {
          ...transaction,
          id: Date.now().toString(),
        };
        
        set((state) => {
          const newTransactions = [newTransaction, ...state.transactions];
          return {
            transactions: newTransactions,
            balance: calculateBalance(newTransactions),
          };
        });
      },

      updateTransaction: (id, updates) => {
        set((state) => {
          const updatedTransactions = state.transactions.map(t =>
            t.id === id ? { ...t, ...updates } : t
          );
          return {
            transactions: updatedTransactions,
            balance: calculateBalance(updatedTransactions),
          };
        });
      },

      deleteTransaction: (id) => {
        set((state) => {
          const filteredTransactions = state.transactions.filter(t => t.id !== id);
          return {
            transactions: filteredTransactions,
            balance: calculateBalance(filteredTransactions),
          };
        });
      },

      addBudget: (budget) => {
        const newBudget: Budget = {
          ...budget,
          id: Date.now().toString(),
          spent: 0,
        };
        
        set((state) => ({
          budgets: [...state.budgets, newBudget],
        }));
      },

      updateBudget: (id, updates) => {
        set((state) => ({
          budgets: state.budgets.map(b =>
            b.id === id ? { ...b, ...updates } : b
          ),
        }));
      },

      deleteBudget: (id) => {
        set((state) => ({
          budgets: state.budgets.filter(b => b.id !== id),
        }));
      },

      getAnalytics: (): AnalyticsData => {
        const { transactions } = get();
        return {
          totalIncome: calculateTotalByType(transactions, 'income'),
          totalExpenses: calculateTotalByType(transactions, 'expense'),
          balance: calculateBalance(transactions),
          categorySpending: calculateCategorySpending(transactions),
          monthlyTrends: getMonthlyTrends(transactions),
        };
      },

      clearAllData: () => {
        set({
          transactions: [],
          budgets: [],
          balance: 0,
        });
      },
    }),
    {
      name: 'wallet-storage',
      storage: {
        getItem: async (name) => {
          const value = await AsyncStorage.getItem(name);
          return value ? JSON.parse(value) : null;
        },
        setItem: async (name, value) => {
          await AsyncStorage.setItem(name, JSON.stringify(value));
        },
        removeItem: async (name) => {
          await AsyncStorage.removeItem(name);
        },
      },
    }
  )
);