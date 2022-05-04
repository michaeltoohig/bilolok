/* eslint-disable */
import usersApi from '@/api/users.js';
import { getDarkMode, saveDarkMode, getLocale, saveLocale } from '@/utils.js';

const initialState = () => ({
  darkMode: false,
  locale: 'bi',
});

const state = initialState();

const getters = {
  darkMode: (state) => {
    return state.darkMode;
  },
};

const actions = {
  setDarkMode: async ({ commit }, dark) => {
    saveDarkMode(dark);
    commit('setDarkMode', dark);
  },
  checkDarkMode({ commit }) {
    const dark = getDarkMode();
    commit('setDarkMode', dark);
  },
  setLocale: async ({ commit }, locale) => {
    saveLocale(locale);
    commit('setLocale', locale);
  },
  checkLocale({ commit }) {
    const locale = getLocale();
    commit('setLocale', locale);
  },
};

const mutations = {
  RESET(state) {
    const newState = initialState();
    Object.keys(newState).forEach(key => {
      state[key] = newState[key];
    });
  },
  // TODO update below to be same as pattern seen in other modules
  setDarkMode(state, dark) {
    state.darkMode = dark;
  },
  setLocale(state, locale) {
    state.locale = locale;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
