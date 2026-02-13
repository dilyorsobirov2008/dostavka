/**
 * TMA Utilities - Telegram Mini App SDK-bilan ishlash
 */

import { initializeApp, useMainButton, useHapticFeedback } from '@telegram-apps/sdk';

// Telegram SDK ni ishga tushirish
export const initTMA = () => {
  try {
    const tmaSDK = initializeApp();
    return {
      sdk: tmaSDK,
      user: tmaSDK.initDataUnsafe?.user,
      chatInstance: tmaSDK.initDataUnsafe?.chat_instance,
      initData: tmaSDK.initData
    };
  } catch (error) {
    console.log('TMA SDK initialization error:', error);
    return null;
  }
};

// Main Button - Buyurtma berish tugmasi
export const setupMainButton = (onClick) => {
  try {
    const mainButton = useMainButton();
    mainButton.setText('Buyurtmani yuborish');
    mainButton.onClick(onClick);
    mainButton.show();
    return mainButton;
  } catch (error) {
    console.log('Main button setup error:', error);
  }
};

// Haptic Feedback - Vibration
export const triggerHaptic = (type = 'light') => {
  try {
    const haptic = useHapticFeedback();
    
    switch (type) {
      case 'light':
        haptic.impactOccurred('light');
        break;
      case 'medium':
        haptic.impactOccurred('medium');
        break;
      case 'heavy':
        haptic.impactOccurred('heavy');
        break;
      case 'success':
        haptic.notificationOccurred('success');
        break;
      case 'error':
        haptic.notificationOccurred('error');
        break;
      case 'warning':
        haptic.notificationOccurred('warning');
        break;
      default:
        haptic.impactOccurred('light');
    }
  } catch (error) {
    console.log('Haptic feedback error:', error);
  }
};

// Foydalanuvchi ma'lumotlarini olish
export const getUserInfo = () => {
  const tmaSDK = initializeApp();
  const user = tmaSDK.initDataUnsafe?.user;
  
  return {
    id: user?.id,
    firstName: user?.first_name,
    lastName: user?.last_name,
    username: user?.username,
    photoUrl: user?.photo_url,
    isBot: user?.is_bot,
    isPremium: user?.is_premium
  };
};

// Shahar/Davlat ma'lumotlari (agar mavjud bo'lsa)
export const getDeviceInfo = () => {
  const tmaSDK = initializeApp();
  const platform = tmaSDK.platform;
  
  return {
    platform: platform, // 'ios', 'android', 'web', etc.
    isDarkMode: tmaSDK.isDarkMode,
    colorScheme: tmaSDK.colorScheme
  };
};

// Orqaga qaytish tugmasi
export const setupBackButton = (onBack) => {
  try {
    const backButton = useBackButton();
    backButton.show();
    backButton.onClick(onBack);
    return backButton;
  } catch (error) {
    console.log('Back button setup error:', error);
  }
};

// Telegram'da linerni ochish
export const openLink = (url) => {
  try {
    const web = useWebApp();
    web.openLink(url);
  } catch (error) {
    console.log('Open link error:', error);
  }
};

// Loading indikator
export const showLoading = (text = 'Yuklanmoqda...') => {
  try {
    const web = useWebApp();
    web.showPopup({
      title: 'Iltimos kutib turing',
      message: text
    });
  } catch (error) {
    console.log('Loading error:', error);
  }
};

// Success/Error va'da-i
export const showAlert = (message) => {
  alert(message);
};

export const showConfirm = (message) => {
  return confirm(message);
};

// Tema ranglarini olish
export const getThemeColors = () => {
  const tmaSDK = initializeApp();
  
  return {
    bgColor: tmaSDK.backgroundColor,
    textColor: tmaSDK.textColor,
    hintColor: tmaSDK.hintColor,
    linkColor: tmaSDK.linkColor,
    buttonColor: tmaSDK.buttonColor,
    buttonTextColor: tmaSDK.buttonTextColor,
    headerBgColor: tmaSDK.headerBgColor,
    sectionBgColor: tmaSDK.sectionBgColor
  };
};

export default {
  initTMA,
  setupMainButton,
  triggerHaptic,
  getUserInfo,
  getDeviceInfo,
  setupBackButton,
  openLink,
  showLoading,
  showAlert,
  showConfirm,
  getThemeColors
};
