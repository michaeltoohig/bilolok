/* eslint-disable */
import router from '@/router';
import { getLocalToken, saveLocalToken, removeLocalToken, getDeviceId } from '@/utils.js';
import authApi from '@/api/auth.js';
import subscriptionsApi from '@/api/subscriptions.js';
import usersApi from '@/api/users.js';

const initialState = function () {
  return {
    isLoggedIn: null,
    logInError: false,
    token: null,
    user: null,
    showAuthModal: false,
    showUserVerifiedModal: false,
  }
};

const state = initialState();

const getters = {
  hasAdminAccess: (state) => {
    return (
      state.user &&
      state.user.is_superuser && state.user.is_active);
  },
  loginError: (state) => state.logInError,
  user: (state) => state.user,
  token: (state) => state.token,
  isLoggedIn: (state) => state.isLoggedIn,
  isUserVerified: (state) => state.isLoggedIn && state.user && state.user.is_verified,
  showAuthModal: (state) => state.showAuthModal,
  showUserVerifiedModal: (state) => state.showUserVerifiedModal,
}

const actions = {
  register: async ({ commit, dispatch }, payload) => {
    try {
      const { data } = await authApi.register(payload);
      // TODO check registration is good and make redirect action
      router.push({ name: 'Auth', params: { auth: 'login' } });
      dispatch('notify/add', {
        title: 'Registration Success',
        text: 'Please log in now.',
        type: 'primary',
        duration: 15_000,
      }, { root: true });
    }
    catch(error) {
      dispatch('notify/add', {
        title: 'Registration Error',
        text: error.response.data.detail,
        type: 'warning',
      }, { root: true });
    }
  },
  jwtLogin: async ({ commit, dispatch }, payload) => {
    try {
      const response = await authApi.login(payload);
      const token = response.data.access_token;
      if (token) {
        saveLocalToken(token);
        commit('setToken', token);
        await dispatch('getMe');
        commit('setLoggedIn', true);
        commit('setLogInError', false);
        await dispatch('routeLoggedIn');
        dispatch('notify/add', {
          title: 'Log In Success',
          text: 'Welcome back.',
          type: 'primary',
          duration: 3_000,
        }, { root: true });
      }
      else {
        await dispatch('logOut');
      }
    }
    catch (error) {
      dispatch('notify/add', {
        title: 'Login Error',
        text: error.response.data.detail,
        type: 'warning',
      }, { root: true });
      commit('setLogInError', true);
      await dispatch('logOut');
    }
  },
  getMe: async ({ commit, dispatch, getters }) => {
    try {
      const response = await usersApi.getMe(getters.token);
      if (response.data) {
        await dispatch('user/getOne', response.data.id, { root: true });
        commit('setUserProfile', response.data);
      }
    } catch (error) {
      await dispatch('checkApiError', error);
    }
  },
  // async actionUpdateUserProfile(context: MainContext, payload) {
  //   try {
  //     const loadingNotification = { content: 'saving', showProgress: true };
  //     commitAddNotification(context, loadingNotification);
  //     const response = (await Promise.all([
  //       api.updateMe(context.state.token, payload),
  //       await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
  //     ]))[0];
  //     commitSetUserProfile(context, response.data);
  //     commitRemoveNotification(context, loadingNotification);
  //     commitAddNotification(context, { content: 'Profile successfully updated', color: 'success' });
  //   } catch (error) {
  //     await dispatchCheckApiError(context, error);
  //   }
  // },
  async checkLoggedIn({ commit, dispatch, getters }) {
    if (!getters.isLoggedIn) {
      let token = getters.token;
      if (!token) {
        const localToken = getLocalToken();
        if (localToken) {
          commit('setToken', localToken);
          token = localToken;
        }
      }
      if (token) {
        try {
          const response = await usersApi.getMe(token);
          await dispatch('user/getOne', response.data.id, { root: true });
          commit('setLoggedIn', true);
          commit('setUserProfile', response.data);
        } catch (error) {
          await dispatch('removeLogIn');
        }
      } else {
        await dispatch('removeLogIn');
      }
    }
  },
  removeLogIn: async ({ commit, getters }) => {
    const deviceId = getDeviceId();
    const token = getters.token;
    if (token && deviceId) {
      // May not need try/catch - testing because of errors reported point here
      try {
        await subscriptionsApi.remove(token, deviceId);
      }
      catch (error) {
        console.log('Error removing subscription');
      }
    }
    removeLocalToken();
    commit('setToken', '');
    commit('setLoggedIn', false);
    commit('setUserProfile', null);
  },
  logOut: async ({ dispatch }) => {
    await dispatch('removeLogIn');
    await dispatch('routeLogOut');
  },
  async userLogOut({ dispatch }) {
    dispatch('logOut');
    dispatch('notify/add', {
      title: 'Logged Out',
      text: 'See you later.',
      type: 'primary',
      duration: 5_000,
    }, { root: true });
  },
  routeLogOut() {
    if (router.currentRoute.path !== '/auth/login') {
      router.push('/auth/login');
    }
  },
  checkApiError: async ({ dispatch }, payload) => {
    if (payload.response?.status === 401) {
      await dispatch('logOut');
    }
  },
  routeLoggedIn() {
    if (router.currentRoute.path === '/auth/login' || router.currentRoute.path === '/') {
      router.push('/');
    }
  },
  // async passwordRecovery(context: MainContext, payload: { username: string }) {
  //   const loadingNotification = { content: 'Sending password recovery email', showProgress: true };
  //   try {
  //     commitAddNotification(context, loadingNotification);
  //     const response = (await Promise.all([
  //       api.passwordRecovery(payload.username),
  //       await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
  //     ]))[0];
  //     commitRemoveNotification(context, loadingNotification);
  //     commitAddNotification(context, { content: 'Password recovery email sent', color: 'success' });
  //     await dispatchLogOut(context);
  //   } catch (error) {
  //     commitRemoveNotification(context, loadingNotification);
  //     commitAddNotification(context, { color: 'error', content: 'Incorrect username' });
  //   }
  // },
  // async resetPassword(context: MainContext, payload: { password: string, token: string }) {
  //   const loadingNotification = { content: 'Resetting password', showProgress: true };
  //   try {
  //     commitAddNotification(context, loadingNotification);
  //     const response = (await Promise.all([
  //       api.resetPassword(payload.password, payload.token),
  //       await new Promise((resolve, reject) => setTimeout(() => resolve(), 500)),
  //     ]))[0];
  //     commitRemoveNotification(context, loadingNotification);
  //     commitAddNotification(context, { content: 'Password successfully reset', color: 'success' });
  //     await dispatchLogOut(context);
  //   } catch (error) {
  //     commitRemoveNotification(context, loadingNotification);
  //     commitAddNotification(context, { color: 'error', content: 'Error resetting password' });
  //   }
  // },
  requestVerification: async ({ dispatch, getters }) => {
    await authApi.requestVerification(getters.user.email);
    dispatch('notify/add', {
      title: 'Email Verification Sent',
      text: 'Please check your inbox for the link to verify your email.',
      type: 'info',
      duration: 10_000,
    }, { root: true });
  },
  verify: async ({ dispatch }, token) => {
    try {
      await authApi.verify(token);
      dispatch('notify/add', {
        title: 'Email Verified',
        text: 'You email has been verified. You may now upload images, check-in, add kava bars to the map, etc.',
        type: 'success',
        duration: 10_000,
      }, { root: true });
      dispatch('getMe');
    }
    catch (error) {
      dispatch('notify/add', {
        title: 'Email Verification Error',
        text: error.response.data.detail,
        type: 'warning',
      }, { root: true });
    }
  },
  setShowAuthModal: async ({ commit }, show) => {
    commit('setShowAuthModal', show);
  },
  setShowUserVerifiedModal: async ({ commit, getters }, show) => {
    if (!getters.isLoggedIn) {
      commit('setShowAuthModal', true);
    } else {
      commit('setShowUserVerifiedModal', show);
    }
  },
};

const mutations = {
  RESET(state) {
    const newState = initialState()
    Object.keys(newState).forEach(key => {
      state[key] = newState[key]
    })
  },
  setToken(state, payload) {
    state.token = payload;
  },
  setLoggedIn(state, payload) {
    state.isLoggedIn = payload;
  },
  setLogInError(state, payload) {
    state.logInError = payload;
  },
  setUserProfile(state, payload) {
    state.user = payload;
  },
  setShowAuthModal(state, show) {
    state.showAuthModal = show;
  },
  setShowUserVerifiedModal(state, show) {
    state.showUserVerifiedModal = show;
  },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
