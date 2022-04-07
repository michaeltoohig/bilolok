/* eslint-disable */

import { getDeviceId, saveDeviceId } from './utils';

export function uuid() {
  let uuidValue = '';
  let randomValue = '';
  let k = 0;
  for (k = 0; k < 32; k += 1) {
    randomValue = Math.random() * 16 | 0;

    if (k === 8 || k === 12 || k === 16 || k === 20) {
      uuidValue += "-"
    }
    uuidValue += (k === 12 ? 4 : (k === 16 ? (randomValue & 3 | 8) : randomValue)).toString(16);
  }
  return uuidValue;
};

let deviceId = getDeviceId();
if (deviceId === null) {
  deviceId = uuid()
  saveDeviceId(deviceId);
}

export default deviceId;
