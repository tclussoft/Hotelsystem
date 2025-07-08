import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { TransactionCategory } from '@/types';
import { getCategoryInfo } from '@/constants/categories';
import { Colors } from '@/constants/colors';

interface CategoryIconProps {
  category: TransactionCategory;
  size?: number;
  showBackground?: boolean;
  backgroundColor?: string;
  iconColor?: string;
}

export const CategoryIcon: React.FC<CategoryIconProps> = ({
  category,
  size = 24,
  showBackground = true,
  backgroundColor,
  iconColor = Colors.text,
}) => {
  const categoryInfo = getCategoryInfo(category);
  const bgColor = backgroundColor || categoryInfo.color;

  const containerStyle = [
    styles.container,
    {
      width: size * 1.5,
      height: size * 1.5,
      borderRadius: (size * 1.5) / 2,
      backgroundColor: showBackground ? bgColor : 'transparent',
    },
  ];

  return (
    <View style={containerStyle}>
      <Ionicons
        name={categoryInfo.icon as any}
        size={size}
        color={showBackground ? Colors.text : iconColor}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
  },
});