module.exports = {
  preset: 'react-native',
  testEnvironment: 'node',                 // 关键：用 Node 环境
  setupFilesAfterEnv: ['<rootDir>/test/setup-dom.js'],
  transform: { '^.+\\.[jt]sx?$': 'babel-jest' },
  // 静态资源映射，避免旧 asset transformer
  moduleNameMapper: { '\\.(png|jpe?g|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js' },
};

const { JSDOM } = require('jsdom');

beforeEach(() => {
  const { window } = new JSDOM('', { url: 'http://localhost' });
  global.window = window;
  global.document = window.document;
  global.navigator = { userAgent: 'node.js' };

  // 常用补丁
  global.requestAnimationFrame = cb => setTimeout(cb, 0);
  window.matchMedia = window.matchMedia || (() => ({ matches: false, addListener() {}, removeListener() {} }));
  // 如需 fetch：
  if (!global.fetch) global.fetch = (...args) => Promise.reject(new Error('mock me'));
});

afterEach(() => {
  // 清理，防止泄漏
  delete global.window;
  delete global.document;
  delete global.navigator;
  delete global.fetch;
});





// jest.config.js
module.exports = {
  preset: 'react-native',
  testEnvironment: 'jsdom',

  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],

  // 只用 babel-jest；不要引用 node_modules 的绝对路径
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },

  // 忽略大多数 node_modules，只对白名单 RN 生态包做转译（避免把 jest 自身编译了）
  transformIgnorePatterns: [
    'node_modules/(?!(?:' +
      'react-native(?:-.+)?' +                 // react-native 与 react-native-*
      '|@react-native(?:-.+)?' +               // @react-native/*
      '|@react-native-community(?:-.+)?' +     // @react-native-community/*
      '|@react-navigation(?:-.+)?' +           // @react-navigation/*
      ')/)',
  ],

  // 静态资源直接映射，别用 RN 旧的 assetFileTransformer
  moduleNameMapper: {
    '\\.(png|jpe?g|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js',
    'react-native$': require.resolve('react-native'),
  },

  setupFiles: ['<rootDir>/jest/setup.js'],      // 见下
  cacheDirectory: '.jest/cache',
};




