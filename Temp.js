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
