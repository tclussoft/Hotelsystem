# Wallet Tracker 💰

A beautiful and intuitive expense tracking app built with React Native Expo, featuring iOS-inspired design and comprehensive financial management tools.

## ✨ Features

- **Beautiful iOS-Inspired Design**: Clean, minimalist UI with pastel colors and smooth animations
- **Transaction Management**: Add, edit, and categorize income and expenses
- **Visual Analytics**: Interactive charts showing spending patterns and trends
- **Category System**: 15+ predefined categories with custom icons and colors
- **Budget Tracking**: Set and monitor spending limits by category
- **Data Persistence**: Local storage with AsyncStorage and Zustand state management
- **Search & Filter**: Powerful transaction filtering and search capabilities
- **Responsive Design**: Optimized for various screen sizes

## 🎨 Design Philosophy

The app follows iOS design principles with:
- **Soft Color Palette**: Primary blues and mint greens with pastel accents
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Generous white space and consistent padding
- **Components**: Reusable UI components with consistent styling
- **Animations**: Subtle transitions and haptic feedback

## 🏗️ Technical Architecture

### Core Technologies
- **React Native Expo**: Cross-platform mobile development
- **TypeScript**: Type-safe development
- **Zustand**: Lightweight state management with persistence
- **AsyncStorage**: Local data storage
- **Expo Router**: File-based navigation
- **React Native Chart Kit**: Beautiful charts and analytics

### Project Structure
```
wallet-tracker/
├── app/                    # Expo Router screens
│   ├── (tabs)/            # Tab navigation screens
│   │   ├── index.tsx      # Dashboard
│   │   ├── transactions.tsx
│   │   ├── analytics.tsx
│   │   └── settings.tsx
│   ├── transaction/       # Transaction management
│   │   ├── add.tsx
│   │   └── [id].tsx
│   └── _layout.tsx        # Root layout
├── components/            # Reusable UI components
│   ├── ui/               # Basic UI components
│   ├── dashboard/        # Dashboard-specific components
│   └── transactions/     # Transaction components
├── constants/            # App constants
│   ├── colors.ts
│   └── categories.ts
├── store/               # State management
│   └── walletStore.ts
├── types/               # TypeScript definitions
│   └── index.ts
└── utils/               # Helper functions
    ├── formatters.ts
    └── calculations.ts
```

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn
- Expo CLI: `npm install -g @expo/cli`
- iOS Simulator (for iOS development) or Android Studio (for Android)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wallet-tracker
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```

4. **Run on device/simulator**
   - **iOS**: Press `i` in the terminal or scan QR code with Camera app
   - **Android**: Press `a` in the terminal or scan QR code with Expo Go app
   - **Web**: Press `w` in the terminal

## 📱 App Screens

### 🏠 Dashboard
- **Balance Overview**: Total balance with income/expense breakdown
- **Quick Actions**: Fast access to add transactions
- **Recent Transactions**: Latest 5 transactions with details
- **Beautiful Gradient Card**: Eye-catching balance display

### 📋 Transactions
- **Complete Transaction List**: All transactions with search and filtering
- **Category Filtering**: Filter by income, expenses, or specific categories
- **Search Functionality**: Find transactions by title or description
- **Transaction Details**: Tap to view/edit individual transactions

### 📊 Analytics
- **Spending Insights**: Visual breakdown of expenses by category
- **Trend Analysis**: Monthly income vs expenses chart
- **Category Breakdown**: Detailed spending percentages
- **Interactive Charts**: Line charts and pie charts for data visualization

### ⚙️ Settings
- **Data Management**: Export, backup, and clear data options
- **App Information**: Version details and transaction count
- **Support Options**: Help, contact, and rating features

## 🎨 Color Palette

```typescript
Primary Colors:
- Blue: #5B9BD5 (Soft, professional blue)
- Mint: #70D0A4 (Fresh, modern green)

Background:
- Light: #F8FAFC (Clean white-gray)
- Surface: #FFFFFF (Pure white)

Text:
- Primary: #1E293B (Dark slate)
- Secondary: #64748B (Medium gray)
- Tertiary: #94A3B8 (Light gray)

Status Colors:
- Success: #10B981 (Income green)
- Error: #EF4444 (Expense red)
- Warning: #F59E0B (Alert orange)
```

## 🔧 Configuration

### TypeScript Setup
The app uses strict TypeScript with proper path aliases:
```json
{
  "@/*": ["./*"],
  "@/components/*": ["./components/*"],
  "@/constants/*": ["./constants/*"],
  "@/store/*": ["./store/*"],
  "@/types/*": ["./types/*"],
  "@/utils/*": ["./utils/*"]
}
```

### Metro Configuration
Custom Metro config for path resolution:
```javascript
config.resolver.alias = {
  '@': '.',
  '@/components': './components',
  '@/constants': './constants',
  '@/store': './store',
  '@/types': './types',
  '@/utils': './utils',
};
```

## 📝 Usage Examples

### Adding a Transaction
```typescript
// Using the store
const { addTransaction } = useWalletStore();

addTransaction({
  title: 'Coffee Shop',
  amount: 4.50,
  type: 'expense',
  category: 'food',
  date: new Date().toISOString(),
  description: 'Morning coffee'
});
```

### Getting Analytics
```typescript
const { getAnalytics } = useWalletStore();
const analytics = getAnalytics();

console.log(analytics.totalIncome); // Total income
console.log(analytics.totalExpenses); // Total expenses
console.log(analytics.categorySpending); // Spending by category
```

## 🧪 Development

### Available Scripts
- `npm start`: Start Expo development server
- `npm run android`: Run on Android
- `npm run ios`: Run on iOS
- `npm run web`: Run on web

### Code Style
- **TypeScript**: Strict typing throughout
- **ESLint**: Code linting and formatting
- **Consistent Naming**: PascalCase for components, camelCase for functions
- **Component Structure**: Props interface, component, styles

### Adding New Features
1. Create types in `types/index.ts`
2. Add store logic in `store/walletStore.ts`
3. Create components in appropriate directories
4. Add screens to `app/` directory
5. Update navigation if needed

## 🔮 Future Enhancements

- **Cloud Sync**: Backup data to cloud services
- **Multiple Currencies**: Support for different currencies
- **Budget Alerts**: Notifications for budget limits
- **Recurring Transactions**: Automatic transaction scheduling
- **Export Options**: PDF reports and CSV exports
- **Dark Mode**: Toggle between light and dark themes
- **Biometric Security**: Face ID/Touch ID protection
- **Investment Tracking**: Portfolio management features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Expo Team**: For the amazing development platform
- **React Native Community**: For excellent components and libraries
- **Design Inspiration**: iOS design guidelines and modern fintech apps

---

**Made with ❤️ for better financial management**