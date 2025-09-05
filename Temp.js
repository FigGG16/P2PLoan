
import { useEffect, useMemo, useRef, useState, useCallback } from 'react';
import { Platform } from 'react-native';
import Orientation, {
  OrientationLocker,
  OrientationType,        // 'PORTRAIT' | 'LANDSCAPE-LEFT' | 'LANDSCAPE-RIGHT' | 'PORTRAIT-UPSIDEDOWN' | 'FACE-UP' | 'FACE-DOWN' | 'UNKNOWN'
} from 'react-native-orientation-locker';

type UILike = 'portrait' | 'landscape' | 'unknown';

/**
 * 将库的枚举值收敛为简化态（portrait/landscape/unknown）
 */
function toSimple(o?: OrientationType | null): UILike {
  switch (o) {
    case 'PORTRAIT':
    case 'PORTRAIT-UPSIDEDOWN':
      return 'portrait';
    case 'LANDSCAPE-LEFT':
    case 'LANDSCAPE-RIGHT':
      return 'landscape';
    default:
      return 'unknown';
  }
}

export interface UseOrientationResult {
  /** UI 层实际方向（受系统旋转开关 & 导航栈/库锁定影响） */
  uiOrientation: OrientationType | 'UNKNOWN';
  /** 设备物理方向（更贴近传感器，不一定等于 UI） */
  deviceOrientation: OrientationType | 'UNKNOWN';
  /** 简化版（基于 UI） */
  simple: UILike;
  /** 是否处于库层锁定（lockToXXX 之后直到 unlockAllOrientations） */
  lockedByLibrary: boolean;
  /** Android：系统“自动旋转”是否开启；iOS 固定为 undefined */
  autoRotateEnabled?: boolean;
  /** 便捷布尔 */
  isPortrait: boolean;
  isLandscape: boolean;

  /** 可选的快捷方法（由调用方决定是否使用） */
  lockToPortrait: () => void;
  lockToLandscape: () => void;
  unlockAll: () => void;
}

export function useOrientation(): UseOrientationResult {
  const [uiOrientation, setUiOrientation] = useState<OrientationType | 'UNKNOWN'>('UNKNOWN');
  const [deviceOrientation, setDeviceOrientation] = useState<OrientationType | 'UNKNOWN'>('UNKNOWN');
  const [lockedByLibrary, setLockedByLibrary] = useState<boolean>(false);
  const [autoRotateEnabled, setAutoRotateEnabled] = useState<boolean | undefined>(
    Platform.OS === 'android' ? false : undefined
  );

  // 稳定的回调引用，便于 removeListener
  const uiListenerRef = useRef<(o: OrientationType) => void>();
  const deviceListenerRef = useRef<(o: OrientationType) => void>();
  const lockListenerRef = useRef<(o: OrientationType | 'UNKNOWN') => void>();

  useEffect(() => {
    // 1) 拉取初始值（UI & Device）
    Orientation.getOrientation((o) => setUiOrientation(o ?? 'UNKNOWN'));
    Orientation.getDeviceOrientation((o) => setDeviceOrientation(o ?? 'UNKNOWN'));

    // 2) Android：读取系统“自动旋转”总开关
    if (Platform.OS === 'android') {
      Orientation.getAutoRotateState?.((state: boolean) => setAutoRotateEnabled(!!state));
    }

    // 3) 锁定状态（库层）
    Orientation.isLocked?.().then?.((isLocked: boolean) => {
      if (typeof isLocked === 'boolean') setLockedByLibrary(isLocked);
    });

    // 4) 订阅监听
    uiListenerRef.current = (o) => setUiOrientation(o ?? 'UNKNOWN');
    deviceListenerRef.current = (o) => setDeviceOrientation(o ?? 'UNKNOWN');
    lockListenerRef.current = (o) => {
      // o === 'UNKNOWN' 表示未被库锁定
      setLockedByLibrary(o !== 'UNKNOWN');
      // 解锁/切换时库会重发一次 UI 方向，保持与 README 行为一致
      // 无需手动更新 uiOrientation
    };

    if (uiListenerRef.current) Orientation.addOrientationListener(uiListenerRef.current);
    if (deviceListenerRef.current) Orientation.addDeviceOrientationListener(deviceListenerRef.current);
    if (lockListenerRef.current) Orientation.addLockListener(lockListenerRef.current);

    // 清理
    return () => {
      if (uiListenerRef.current) Orientation.removeOrientationListener(uiListenerRef.current);
      if (deviceListenerRef.current) Orientation.removeDeviceOrientationListener(deviceListenerRef.current);
      if (lockListenerRef.current) Orientation.removeLockListener(lockListenerRef.current);
      Orientation.removeAllListeners?.(); // 旧版本提供，安全冗余
    };
  }, []);

  const simple = useMemo<UILike>(() => toSimple(uiOrientation), [uiOrientation]);

  const isPortrait = simple === 'portrait';
  const isLandscape = simple === 'landscape';

  // 可选：向外暴露锁定/解锁的便捷方法
  const lockToPortrait = useCallback(() => {
    Orientation.lockToPortrait();
  }, []);
  const lockToLandscape = useCallback(() => {
    Orientation.lockToLandscape();
  }, []);
  const unlockAll = useCallback(() => {
    Orientation.unlockAllOrientations();
  }, []);

  return {
    uiOrientation,
    deviceOrientation,
    simple,
    lockedByLibrary,
    autoRotateEnabled,
    isPortrait,
    isLandscape,
    lockToPortrait,
    lockToLandscape,
    unlockAll,
  };
}



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
