import { Transaction, TransactionCategory, AnalyticsData } from '@/types';

export const calculateBalance = (transactions: Transaction[]): number => {
  return transactions.reduce((balance, transaction) => {
    return transaction.type === 'income' 
      ? balance + transaction.amount 
      : balance - transaction.amount;
  }, 0);
};

export const calculateTotalByType = (
  transactions: Transaction[], 
  type: 'income' | 'expense'
): number => {
  return transactions
    .filter(t => t.type === type)
    .reduce((total, t) => total + t.amount, 0);
};

export const calculateCategorySpending = (
  transactions: Transaction[]
): Record<TransactionCategory, number> => {
  const spending: Record<string, number> = {};
  
  transactions
    .filter(t => t.type === 'expense')
    .forEach(transaction => {
      spending[transaction.category] = (spending[transaction.category] || 0) + transaction.amount;
    });
    
  return spending as Record<TransactionCategory, number>;
};

export const getMonthlyTrends = (transactions: Transaction[]) => {
  const monthlyData: Record<string, { income: number; expenses: number }> = {};
  
  transactions.forEach(transaction => {
    const date = new Date(transaction.date);
    const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    
    if (!monthlyData[monthKey]) {
      monthlyData[monthKey] = { income: 0, expenses: 0 };
    }
    
    if (transaction.type === 'income') {
      monthlyData[monthKey].income += transaction.amount;
    } else {
      monthlyData[monthKey].expenses += transaction.amount;
    }
  });
  
  return Object.entries(monthlyData)
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-12) // Last 12 months
    .map(([month, data]) => ({
      month: new Date(month + '-01').toLocaleDateString('en-US', { month: 'short' }),
      ...data,
    }));
};

export const getTransactionsForPeriod = (
  transactions: Transaction[],
  period: 'week' | 'month' | 'year'
): Transaction[] => {
  const now = new Date();
  const startDate = new Date();
  
  switch (period) {
    case 'week':
      startDate.setDate(now.getDate() - 7);
      break;
    case 'month':
      startDate.setMonth(now.getMonth() - 1);
      break;
    case 'year':
      startDate.setFullYear(now.getFullYear() - 1);
      break;
  }
  
  return transactions.filter(t => new Date(t.date) >= startDate);
};

export const calculateBudgetProgress = (
  transactions: Transaction[],
  category: TransactionCategory,
  budgetLimit: number,
  period: 'weekly' | 'monthly' | 'yearly'
): { spent: number; remaining: number; percentage: number } => {
  const now = new Date();
  const startDate = new Date();
  
  switch (period) {
    case 'weekly':
      startDate.setDate(now.getDate() - 7);
      break;
    case 'monthly':
      startDate.setMonth(now.getMonth() - 1);
      break;
    case 'yearly':
      startDate.setFullYear(now.getFullYear() - 1);
      break;
  }
  
  const spent = transactions
    .filter(t => 
      t.type === 'expense' && 
      t.category === category && 
      new Date(t.date) >= startDate
    )
    .reduce((total, t) => total + t.amount, 0);
    
  const remaining = Math.max(0, budgetLimit - spent);
  const percentage = budgetLimit > 0 ? (spent / budgetLimit) * 100 : 0;
  
  return { spent, remaining, percentage };
};