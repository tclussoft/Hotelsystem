import { CategoryInfo } from '@/types';
import { Colors } from './colors';

export const CATEGORIES: CategoryInfo[] = [
  {
    id: 'food',
    name: 'Food & Dining',
    icon: 'restaurant',
    color: Colors.categoryColors.food,
  },
  {
    id: 'transport',
    name: 'Transportation',
    icon: 'car',
    color: Colors.categoryColors.transport,
  },
  {
    id: 'shopping',
    name: 'Shopping',
    icon: 'shopping-bag',
    color: Colors.categoryColors.shopping,
  },
  {
    id: 'entertainment',
    name: 'Entertainment',
    icon: 'movie',
    color: Colors.categoryColors.entertainment,
  },
  {
    id: 'bills',
    name: 'Bills & Utilities',
    icon: 'receipt',
    color: Colors.categoryColors.bills,
  },
  {
    id: 'health',
    name: 'Health & Fitness',
    icon: 'medical',
    color: Colors.categoryColors.health,
  },
  {
    id: 'education',
    name: 'Education',
    icon: 'school',
    color: Colors.categoryColors.education,
  },
  {
    id: 'travel',
    name: 'Travel',
    icon: 'airplane',
    color: Colors.categoryColors.travel,
  },
  {
    id: 'groceries',
    name: 'Groceries',
    icon: 'basket',
    color: Colors.categoryColors.groceries,
  },
  {
    id: 'salary',
    name: 'Salary',
    icon: 'card',
    color: Colors.categoryColors.salary,
  },
  {
    id: 'freelance',
    name: 'Freelance',
    icon: 'briefcase',
    color: Colors.categoryColors.freelance,
  },
  {
    id: 'business',
    name: 'Business',
    icon: 'business',
    color: Colors.categoryColors.business,
  },
  {
    id: 'investment',
    name: 'Investment',
    icon: 'trending-up',
    color: Colors.categoryColors.investment,
  },
  {
    id: 'gift',
    name: 'Gift',
    icon: 'gift',
    color: Colors.categoryColors.gift,
  },
  {
    id: 'other',
    name: 'Other',
    icon: 'ellipsis-horizontal',
    color: Colors.categoryColors.other,
  },
];

export const getCategoryInfo = (categoryId: string): CategoryInfo => {
  return CATEGORIES.find(cat => cat.id === categoryId) || CATEGORIES[CATEGORIES.length - 1];
};