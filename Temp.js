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
