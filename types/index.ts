export type TransactionType = 'income' | 'expense';

export type TransactionCategory = 
  | 'food'
  | 'transport'
  | 'shopping'
  | 'entertainment'
  | 'bills'
  | 'health'
  | 'education'
  | 'travel'
  | 'groceries'
  | 'salary'
  | 'freelance'
  | 'business'
  | 'investment'
  | 'gift'
  | 'other';

export interface Transaction {
  id: string;
  title: string;
  amount: number;
  type: TransactionType;
  category: TransactionCategory;
  date: string;
  description?: string;
  location?: string;
}

export interface Budget {
  id: string;
  category: TransactionCategory;
  limit: number;
  spent: number;
  period: 'weekly' | 'monthly' | 'yearly';
}

export interface CategoryInfo {
  id: TransactionCategory;
  name: string;
  icon: string;
  color: string;
}

export interface AnalyticsData {
  totalIncome: number;
  totalExpenses: number;
  balance: number;
  categorySpending: Record<TransactionCategory, number>;
  monthlyTrends: Array<{
    month: string;
    income: number;
    expenses: number;
  }>;
}

export interface WalletState {
  transactions: Transaction[];
  budgets: Budget[];
  balance: number;
  addTransaction: (transaction: Omit<Transaction, 'id'>) => void;
  updateTransaction: (id: string, transaction: Partial<Transaction>) => void;
  deleteTransaction: (id: string) => void;
  addBudget: (budget: Omit<Budget, 'id' | 'spent'>) => void;
  updateBudget: (id: string, budget: Partial<Budget>) => void;
  deleteBudget: (id: string) => void;
  getAnalytics: () => AnalyticsData;
  clearAllData: () => void;
}