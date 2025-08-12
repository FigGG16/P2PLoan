/**
 * jest/setup.rn.js
 * 适配 RN 0.67.x 在 Jest（Node/jsdom）中的常见原生缺口
 */

// --- 基础 polyfill（jsdom/Node 常见缺口） ---
try {
  const { performance } = require('perf_hooks');
  if (!global.performance || !global.performance.now) {
    global.performance = performance;
  }
} catch {}

if (!global.requestAnimationFrame) {
  global.requestAnimationFrame = (cb) => setTimeout(cb, 0);
}
if (typeof window !== 'undefined' && !window.matchMedia) {
  // 极简实现，够大多数库判断用
  window.matchMedia = () => ({
    matches: false,
    addListener() {},
    removeListener() {},
    addEventListener() {},
    removeEventListener() {},
    dispatchEvent() { return false; },
  });
}

// --- RN Animated 的噪音、手势库等 ---
jest.mock('react-native/Libraries/Animated/NativeAnimatedHelper', () => ({}));

// react-native-gesture-handler 官方提供的 jest 初始化
try {
  require('react-native-gesture-handler/jestSetup');
} catch {}

// react-native-reanimated 官方 mock（避免触发原生分支）
jest.mock('react-native-reanimated', () => require('react-native-reanimated/mock'));

// --- TurboModule & NativeModules 缺口（SettingsManager / I18nManager 等） ---
jest.mock('react-native/Libraries/TurboModule/TurboModuleRegistry', () => {
  const actual = jest.requireActual('react-native/Libraries/TurboModule/TurboModuleRegistry');
  return {
    ...actual,
    getEnforcing: (name) => {
      if (name === 'SettingsManager') {
        // iOS 常用字段
        return {
          settings: { AppleLocale: 'en_US', AppleLanguages: ['en-US'] },
          localeIdentifier: 'en_US',
        };
      }
      if (name === 'I18nManager') {
        return { localeIdentifier: 'en_US', isRTL: false, doLeftAndRightSwapInRTL: false };
      }
      return actual.getEnforcing ? actual.getEnforcing(name) : {};
    },
  };
});

// 有些库直接 new NativeEventEmitter()，在 Jest 里需要给个空实现
jest.mock('react-native/Libraries/EventEmitter/NativeEventEmitter', () => {
  return jest.fn().mockImplementation(() => ({
    addListener: jest.fn(),
    removeListener: jest.fn(),
    removeAllListeners: jest.fn(),
    emit: jest.fn(),
    listenerCount: jest.fn(() => 0),
  }));
});

// --- 常见社区库的 mock（按你项目里用到的补充即可） ---

// 1) react-native-device-info
jest.mock('react-native-device-info', () => {
  const api = {
    isTablet: jest.fn(() => false),
    getUniqueId: jest.fn(() => 'mock-uid'),
    getSystemName: jest.fn(() => 'iOS'),
    getSystemVersion: jest.fn(() => '14.4'),
  };
  return { __esModule: true, ...api, default: api };
});

// 2) @react-native-community/netinfo
jest.mock('@react-native-community/netinfo', () => {
  const listeners = new Set();
  const api = {
    addEventListener: jest.fn((type, cb) => {
      listeners.add(cb);
      // 初始派发一次联通状态
      cb({ type: 'wifi', isConnected: true, isInternetReachable: true, details: {} });
      return { remove: () => listeners.delete(cb) };
    }),
    fetch: jest.fn(async () => ({
      type: 'wifi',
      isConnected: true,
      isInternetReachable: true,
      details: {},
    })),
    useNetInfo: jest.fn(() => ({
      type: 'wifi',
      isConnected: true,
      isInternetReachable: true,
      details: {},
    })),
  };
  return { __esModule: true, ...api, default: api };
});

// 3) AsyncStorage（如果用到了）
try {
  jest.mock('@react-native-async-storage/async-storage', () =>
    require('@react-native-async-storage/async-storage/jest/async-storage-mock')
  );
} catch {}
