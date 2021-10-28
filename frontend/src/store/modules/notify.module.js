/* eslint-disable */

const defaultDuration = 8000;

// Valid mutation names
const NOTIFICATION_ADDED = 'NOTIFICATION_ADDED';
const NOTIFICATION_DISMISSED = 'NOTIFICATION_DISMISSED';

const initialState = () => ({
  notifications: [],
});

const state = initialState();

const getters = {
  notifications: (state) => state.notifications.map(n => n.raw),
};

const actions = {
  add: async ({ commit }, notification) => {
    let duration = notification.duration || defaultDuration;
    // create timeout for notification
    var timeOut = setTimeout(() => {
      commit(NOTIFICATION_DISMISSED, notification)
    }, duration);
    // create notification
    commit(NOTIFICATION_ADDED, {
      raw: notification,
      timeOut: timeOut,
    });
  },
  dismiss: async ({ commit }, notification) => {
    commit(NOTIFICATION_DISMISSED, notification);
  },
};

const mutations = {
  [NOTIFICATION_ADDED]: (state, notification) => {
    state.notifications.push(notification);
  },
  [NOTIFICATION_DISMISSED]: (state, rawNotification) => {
    var i = state.notifications.map(n => n.raw).indexOf(rawNotification);
    if (i === -1) return;
    // clear and remove notification
    clearTimeout(state.notifications[i].timeOut);
    state.notifications.splice(i, 1);
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
}