import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useWalletStore } from '@/store/walletStore';
import { Card } from '@/components/ui/Card';
import { Colors } from '@/constants/colors';

interface SettingItemProps {
  title: string;
  description?: string;
  icon: string;
  onPress: () => void;
  variant?: 'default' | 'danger';
}

const SettingItem: React.FC<SettingItemProps> = ({
  title,
  description,
  icon,
  onPress,
  variant = 'default',
}) => {
  const isDestructive = variant === 'danger';
  
  return (
    <TouchableOpacity style={styles.settingItem} onPress={onPress}>
      <View style={styles.settingContent}>
        <View
          style={[
            styles.iconContainer,
            { backgroundColor: isDestructive ? Colors.errorLight : Colors.primary + '20' },
          ]}
        >
          <Ionicons
            name={icon as any}
            size={20}
            color={isDestructive ? Colors.error : Colors.primary}
          />
        </View>
        <View style={styles.textContainer}>
          <Text
            style={[
              styles.settingTitle,
              { color: isDestructive ? Colors.error : Colors.text },
            ]}
          >
            {title}
          </Text>
          {description && (
            <Text style={styles.settingDescription}>{description}</Text>
          )}
        </View>
        <Ionicons
          name="chevron-forward"
          size={20}
          color={Colors.textTertiary}
        />
      </View>
    </TouchableOpacity>
  );
};

export default function SettingsScreen() {
  const { clearAllData, transactions } = useWalletStore();

  const handleClearData = () => {
    Alert.alert(
      'Clear All Data',
      'This action will permanently delete all your transactions and budgets. This cannot be undone.',
      [
        {
          text: 'Cancel',
          style: 'cancel',
        },
        {
          text: 'Delete All',
          style: 'destructive',
          onPress: () => {
            clearAllData();
            Alert.alert('Success', 'All data has been cleared.');
          },
        },
      ]
    );
  };

  const handleExportData = () => {
    Alert.alert(
      'Export Data',
      'This feature will be available in a future update.',
      [{ text: 'OK' }]
    );
  };

  const handleBackupData = () => {
    Alert.alert(
      'Backup Data',
      'This feature will be available in a future update.',
      [{ text: 'OK' }]
    );
  };

  const handleAbout = () => {
    Alert.alert(
      'About Wallet Tracker',
      'Version 1.0.0\n\nA beautiful and intuitive expense tracking app designed to help you manage your finances with ease.',
      [{ text: 'OK' }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>Settings</Text>
        </View>

        {/* Data & Privacy */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Data & Privacy</Text>
          
          <SettingItem
            title="Export Data"
            description="Export your transactions to CSV"
            icon="download-outline"
            onPress={handleExportData}
          />
          
          <SettingItem
            title="Backup Data"
            description="Create a backup of your data"
            icon="cloud-upload-outline"
            onPress={handleBackupData}
          />
          
          <SettingItem
            title="Clear All Data"
            description="Permanently delete all transactions and budgets"
            icon="trash-outline"
            onPress={handleClearData}
            variant="danger"
          />
        </Card>

        {/* App Information */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>App Information</Text>
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>Total Transactions</Text>
            <Text style={styles.infoValue}>{transactions.length}</Text>
          </View>
          
          <View style={styles.infoItem}>
            <Text style={styles.infoLabel}>App Version</Text>
            <Text style={styles.infoValue}>1.0.0</Text>
          </View>
          
          <SettingItem
            title="About"
            description="Learn more about Wallet Tracker"
            icon="information-circle-outline"
            onPress={handleAbout}
          />
        </Card>

        {/* Support */}
        <Card style={styles.section}>
          <Text style={styles.sectionTitle}>Support</Text>
          
          <SettingItem
            title="Help & FAQ"
            description="Get help and find answers"
            icon="help-circle-outline"
            onPress={() => Alert.alert('Help', 'Help documentation coming soon!')}
          />
          
          <SettingItem
            title="Contact Support"
            description="Get in touch with our team"
            icon="mail-outline"
            onPress={() => Alert.alert('Contact', 'Support contact coming soon!')}
          />
          
          <SettingItem
            title="Rate App"
            description="Rate us on the App Store"
            icon="star-outline"
            onPress={() => Alert.alert('Rate App', 'Thank you for using Wallet Tracker!')}
          />
        </Card>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>
            Made with ❤️ for better financial management
          </Text>
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
  section: {
    margin: 16,
    paddingVertical: 8,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: Colors.text,
    marginBottom: 16,
    paddingHorizontal: 8,
  },
  settingItem: {
    paddingVertical: 4,
  },
  settingContent: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 8,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 16,
  },
  textContainer: {
    flex: 1,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: Colors.text,
  },
  settingDescription: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  infoItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 8,
    borderBottomWidth: 1,
    borderBottomColor: Colors.borderLight,
  },
  infoLabel: {
    fontSize: 16,
    color: Colors.text,
  },
  infoValue: {
    fontSize: 16,
    fontWeight: '500',
    color: Colors.textSecondary,
  },
  footer: {
    alignItems: 'center',
    paddingVertical: 24,
    paddingHorizontal: 20,
  },
  footerText: {
    fontSize: 14,
    color: Colors.textTertiary,
    textAlign: 'center',
  },
  bottomSpacing: {
    height: 40,
  },
});