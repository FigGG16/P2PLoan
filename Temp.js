// 在 jest.setup.js 里追加：对 react-native 做“增量 mock”
jest.mock('react-native', () => {
  // 先拿到真实实现
  const RN = jest.requireActual('react-native');

  // 一些常见的 NativeModules 兜底
  const NativeModules = {
    ...RN.NativeModules,
    // 有些库会期望 UIManager 里有 measureLayout 等
    UIManager: {
      ...RN.NativeModules?.UIManager,
      // Fabric/非Fabric 项目都兜一层
      RCTView: RN.NativeModules?.UIManager?.RCTView || {},
      measure: jest.fn(),
      measureInWindow: jest.fn(),
      measureLayout: jest.fn(),
      createView: jest.fn(),
      setChildren: jest.fn(),
      removeSubviewsFromContainer: jest.fn(),
      manageChildren: jest.fn(),
    },
    // 有些库读这个开关
    PlatformConstants: {
      ...RN.NativeModules?.PlatformConstants,
      forceTouchAvailable: false,
      isTesting: true,
      reactNativeVersion: RN.Platform?.version || { major: 0, minor: 0, patch: 0 },
    },
    // 如果项目里用到了 Share/Intent 系列
    IntentAndroid: RN.NativeModules?.IntentAndroid || {},
    // 你项目里涉及的其它原生模块也可以在这里补：
    // MyNativeModule: { foo: jest.fn(), bar: jest.fn() },
  };

  // UIManager 也经常被直接读取
  const UIManager = {
    ...RN.UIManager,
    // 避免某些依赖直接访问 getViewManagerConfig 报错
    getViewManagerConfig: name => ({ Commands: {}, Constants: {}, Manager: name }),
  };

  // 常见 API 的轻量 mock
  const Linking = {
    ...RN.Linking,
    openURL: jest.fn().mockResolvedValue(true),
    canOpenURL: jest.fn().mockResolvedValue(true),
    addEventListener: jest.fn(() => ({ remove: jest.fn() })),
    getInitialURL: jest.fn().mockResolvedValue(null),
  };

  const Clipboard = {
    // expo-clipboard 或 RN Clipboard 取其一；没有就兜底
    ...RN.Clipboard,
    getString: jest.fn().mockResolvedValue(''),
    setString: jest.fn(),
  };

  const Dimensions = {
    ...RN.Dimensions,
    get: jest.fn().mockImplementation(key => {
      // 默认给个 iPhone 常见尺寸
      if (key === 'window' || key === 'screen') {
        return { width: 375, height: 667, scale: 2, fontScale: 2 };
      }
      return { width: 375, height: 667, scale: 2, fontScale: 2 };
    }),
    // 有些库会 subscribe
    addEventListener: jest.fn(() => ({ remove: jest.fn() })),
    removeEventListener: jest.fn(),
  };

  const InteractionManager = {
    ...RN.InteractionManager,
    runAfterInteractions: cb => {
      // 直接同步执行，避免测试里卡住
      if (typeof cb === 'function') cb();
      return { then: fn => fn && fn(), done: () => {}, cancel: () => {} };
    },
  };

  const Appearance = {
    ...RN.Appearance,
    getColorScheme: jest.fn(() => 'light'),
    addChangeListener: jest.fn(() => ({ remove: jest.fn() })),
  };

  const AppState = {
    ...RN.AppState,
    currentState: 'active',
    addEventListener: jest.fn(() => ({ remove: jest.fn() })),
    removeEventListener: jest.fn(),
  };

  return {
    ...RN,
    NativeModules,
    UIManager,
    Linking,
    Clipboard,
    Dimensions,
    InteractionManager,
    Appearance,
    AppState,
    // Platform 也可按需固定到 'ios' 或 'android'
    Platform: { ...RN.Platform, OS: RN.Platform?.OS || 'ios', select: RN.Platform.select },
  };
});
