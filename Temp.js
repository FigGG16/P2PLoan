// OnlyAndroidKeyboardAvoidingView.tsx
import React from 'react';
import { KeyboardAvoidingView, Platform, View, StyleProp, ViewStyle } from 'react-native';

interface Props {
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
  behavior?: 'height' | 'position' | 'padding';
}

export default function OnlyAndroidKeyboardAvoidingView({
  children,
  style,
  behavior = 'height', // Android 上常用 height
}: Props) {
  if (Platform.OS === 'android') {
    return (
      <KeyboardAvoidingView behavior={behavior} style={style} enabled>
        {children}
      </KeyboardAvoidingView>
    );
  }

  // iOS 平台：完全不渲染 KAV
  return <View style={style}>{children}</View>;
}

///-------------
1.对
2.对
3. C (想问 奇异值也可以是是AA^T的特征值的平方根吧)
4.D
5.C
6.
特征向量矩阵是 V 和 V^T , 特征值矩阵是\Sigma, 他与A*v^i = \sigma^i *u^i 的关系是:
相互推到关系，只是为了验证原始中的V 是一个正交矩阵，V与U 可以相互转换
7. 
矩阵A是 4*3 矩阵，秩为2，必定有两列向量张成列空间，而左零空间为 n-r = 1,由剩下的一列张成。
同样， 必定有两行向量张成行空间，而零空间为 m-r = 2, 由剩下的两列张成。
其完整的SVD为 A = U\SigmaV^T = \Sigma_1*u_1*v_1^T + \Sigma_2*u_2*v_2^T (理由是矩阵A的秩为2，所以最多只有2个奇异值)
8. 
解决的核心问题是，A^T * A 可以构造正交（正定）矩阵，并且证明了 Av_i = \Sigma_i *u_i ，并且向量 v_i 与u_i 两两正交，
v_i可以通过A 映射到 u_i, u_i 也可以通过A^T映射成  }
  return results;
}

const results = findDeps(lockData);
console.log(`🔍 找到 ${results.length} 个 lodash 版本：`);
results.forEach(r => {
  console.log(`- ${r.version} @ ${r.package}`);
});
25-乙巳。
26-丙午
27-丁未
28-戊申
29-己酉
3
31-辛亥
32-壬子
33-癸丑
34-甲寅
35-乙卯
36-丙辰
37-丁巳
38-戊午
39-己未
module.exports = {
  preset: 'react-native',
  testEnvironment: 'jsdom',
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],

  // 只用 babel-jest 处理源代码
  transform: {
    '^.+\\.[jt]sx?$': 'babel-jest',
  },

  // ❗不要编译 node_modules，只有 RN 相关库作为白名单
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|react-clone-referenced-element|@react-navigation|react-native-gesture-handler|react-native-reanimated|react-native-safe-area-context|react-native-screens)/)',
  ],

  // 静态资源映射为占位
  moduleNameMapper: {
    '\\.(png|jpe?g|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js',
    'react-native$': require.resolve('react-native'),
  },

  setupFiles: ['<rootDir>/jest/setup.ts'],
  setupFilesAfterEnv: ['<rootDir>/script/jestGlobal.ts'],
  cacheDirectory: '.jest/cache',
};

xxxxxxxx
