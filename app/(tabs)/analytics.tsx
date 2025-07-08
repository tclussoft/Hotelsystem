import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { useWalletStore } from '@/store/walletStore';
import { Card } from '@/components/ui/Card';
import { CategoryIcon } from '@/components/ui/CategoryIcon';
import { formatAmount, formatPercentage } from '@/utils/formatters';
import { Colors } from '@/constants/colors';
import { getCategoryInfo } from '@/constants/categories';

const screenWidth = Dimensions.get('window').width;

export default function AnalyticsScreen() {
  const { getAnalytics } = useWalletStore();
  const analytics = getAnalytics();
  const [selectedPeriod, setSelectedPeriod] = useState<'week' | 'month' | 'year'>('month');

  const categoryData = Object.entries(analytics.categorySpending)
    .filter(([_, amount]) => amount > 0)
    .sort(([_, a], [__, b]) => b - a)
    .slice(0, 6)
    .map(([category, amount]) => ({
      name: getCategoryInfo(category).name,
      population: amount,
      color: getCategoryInfo(category).color,
      legendFontColor: Colors.text,
      legendFontSize: 12,
    }));

  const monthlyData = {
    labels: analytics.monthlyTrends.map(item => item.month),
    datasets: [
      {
        data: analytics.monthlyTrends.map(item => item.income),
        color: () => Colors.income,
        strokeWidth: 3,
      },
      {
        data: analytics.monthlyTrends.map(item => item.expenses),
        color: () => Colors.expense,
        strokeWidth: 3,
      },
    ],
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Analytics</Text>
        </View>

        {/* Overview Stats */}
        <View style={styles.statsContainer}>
          <Card style={styles.statCard}>
            <Text style={styles.statValue}>
              {formatAmount(analytics.totalIncome)}
            </Text>
            <Text style={styles.statLabel}>Total Income</Text>
          </Card>
          
          <Card style={styles.statCard}>
            <Text style={[styles.statValue, { color: Colors.expense }]}>
              {formatAmount(analytics.totalExpenses)}
            </Text>
            <Text style={styles.statLabel}>Total Expenses</Text>
          </Card>
        </View>

        {/* Monthly Trends Chart */}
        {analytics.monthlyTrends.length > 0 && (
          <Card style={styles.chartCard}>
            <Text style={styles.chartTitle}>Income vs Expenses</Text>
            <LineChart
              data={monthlyData}
              width={screenWidth - 64}
              height={220}
              chartConfig={{
                backgroundColor: Colors.surface,
                backgroundGradientFrom: Colors.surface,
                backgroundGradientTo: Colors.surface,
                decimalPlaces: 0,
                color: (opacity = 1) => `rgba(91, 155, 213, ${opacity})`,
                labelColor: () => Colors.textSecondary,
                style: {
                  borderRadius: 16,
                },
                propsForDots: {
                  r: '4',
                  strokeWidth: '2',
                },
              }}
              bezier
              style={styles.chart}
            />
            <View style={styles.chartLegend}>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: Colors.income }]} />
                <Text style={styles.legendText}>Income</Text>
              </View>
              <View style={styles.legendItem}>
                <View style={[styles.legendDot, { backgroundColor: Colors.expense }]} />
                <Text style={styles.legendText}>Expenses</Text>
              </View>
            </View>
          </Card>
        )}

        {/* Category Spending */}
        {categoryData.length > 0 && (
          <Card style={styles.chartCard}>
            <Text style={styles.chartTitle}>Spending by Category</Text>
            <PieChart
              data={categoryData}
              width={screenWidth - 64}
              height={220}
              chartConfig={{
                color: (opacity = 1) => `rgba(91, 155, 213, ${opacity})`,
              }}
              accessor="population"
              backgroundColor="transparent"
              paddingLeft="15"
              center={[10, 0]}
            />
          </Card>
        )}

        {/* Category Breakdown */}
        <Card style={styles.breakdownCard}>
          <Text style={styles.chartTitle}>Category Breakdown</Text>
          {Object.entries(analytics.categorySpending)
            .filter(([_, amount]) => amount > 0)
            .sort(([_, a], [__, b]) => b - a)
            .map(([category, amount]) => (
              <View key={category} style={styles.categoryItem}>
                <View style={styles.categoryInfo}>
                  <CategoryIcon category={category as any} size={16} />
                  <Text style={styles.categoryName}>
                    {getCategoryInfo(category).name}
                  </Text>
                </View>
                <View style={styles.categoryAmount}>
                  <Text style={styles.categoryValue}>
                    {formatAmount(amount)}
                  </Text>
                  <Text style={styles.categoryPercentage}>
                    {formatPercentage(amount, analytics.totalExpenses)}
                  </Text>
                </View>
              </View>
            ))}
        </Card>

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
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: Colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: Colors.text,
  },
  statsContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingTop: 20,
    gap: 16,
  },
  statCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 20,
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: Colors.income,
    marginBottom: 4,
  },
  statLabel: {
    fontSize: 14,
    color: Colors.textSecondary,
  },
  chartCard: {
    margin: 16,
    marginTop: 20,
  },
  chartTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 16,
  },
  chart: {
    borderRadius: 16,
  },
  chartLegend: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 16,
    gap: 24,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  legendDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  legendText: {
    fontSize: 14,
    color: Colors.textSecondary,
  },
  breakdownCard: {
    margin: 16,
  },
  categoryItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.borderLight,
  },
  categoryInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  categoryName: {
    fontSize: 16,
    color: Colors.text,
    marginLeft: 12,
  },
  categoryAmount: {
    alignItems: 'flex-end',
  },
  categoryValue: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  categoryPercentage: {
    fontSize: 12,
    color: Colors.textTertiary,
    marginTop: 2,
  },
  bottomSpacing: {
    height: 40,
  },
});