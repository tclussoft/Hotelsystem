const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.resolver.alias = {
  '@': '.',
  '@/components': './components',
  '@/constants': './constants',
  '@/store': './store',
  '@/types': './types',
  '@/utils': './utils',
};

module.exports = config;