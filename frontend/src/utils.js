export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token) => localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

export const getDarkMode = () => JSON.parse(localStorage.getItem('dark_mode'));

export const saveDarkMode = (dark) => localStorage.setItem('dark_mode', dark);

export const getDeviceId = () => localStorage.getItem('deviceId');

export const saveDeviceId = (deviceId) => localStorage.setItem('deviceId', deviceId);
