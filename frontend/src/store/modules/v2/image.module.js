import Vue from 'vue';
// import ls from 'localstorage-slim';

// import { normalizeRelations, resolveRelations } from '@/store/helpers';
import imagesApi from '@/api/images';
import nakamalsApi from '@/api/nakamals';
import usersApi from '@/api/users';
import i18n from '@/plugins/i18n';

const initialState = () => ({
  byId: {},
  allIds: [],
  // byNakamalId: {},
  // recentIds: [],
});

const state = initialState();

const getters = {
  // Return a single image with the given id.
  get: (state, _, __, rootGetters) => id => {
    return state.byId[id];
  },
  // nakamal: (state, getters) => nakamalId => {
  //   if (!state.byNakamalId[nakamalId]) return [];
  //   return state.byNakamalId[nakamalId].map(id => getters.get(id));
  // },
  // // Return a list of images in the order of `allIds`.
  // list: (state, getters) => {
  //   return state.allIds.map(id => getters.find(id));
  // },
  // // Return a list of recent images. 
  // recent: (state, getters) => {
  //   return state.recentIds.map(id => getters.find(id));
  // },
  // Return a list of images of a user.
  // user: (state, getters) => userId => {
  //   return state.allIds.map(id => getters.find(id)).filter(c => c.user === userId);
  // },
};

// function commitAddImage(image, commit) {
//   // Normalize nested data and swap the image object
//   // in the API response with an ID reference.
//   commit('add', normalizeRelations(image, ['nakamal', 'user']));
//   // Add or update the image relations.
//   // if (image.nakamal.chief) {
//   //   commit('user/setUser', image.nakamal.chief, {
//   //     root: true,
//   //   });
//   // }
//   // commit('nakamal/add', normalizeRelations(image.nakamal, ['chief']), {
//   //   root: true,
//   // });
//   // commit('user/setUser', image.user, {
//   //   root: true,
//   // });
// };

const actions = {
  fetch: async ({ commit, getters }, id) => {
    try {
      const resp = await imagesApi.get(id);
      // image = resp.data;
      // commitAddImage(image, commit);
      commit('ADD', resp.data);
    } catch (err) {
      console.error('image load error', err);
      throw err;
    }
    // return Promise.resolve(getters.find(id));
  },
  // loadOne: async ({ commit, getters }, id) => {
  //   // TODO handle network errors
  //   let image;
  //   const cacheKey = `images:${id}`;
  //   const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
  //   if (cached) {
  //     image = cached;
  //   } else {
  //     let resp = await imagesApi.get(id);
  //     image = resp.data;
  //     // ls.set(cacheKey, image, { ttl: 900 });
  //   }
  //   commitAddImage(image, commit);
  //   return Promise.resolve(getters.find(id));
  // },
  // getRecent: async ({ commit }) => {
  //   let items;
  //   const cacheKey = 'images:recent';
  //   const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
  //   if (cached) {
  //     return;
  //   } else {
  //     const resp = await imagesApi.getRecent();
  //     items = resp.data;
  //     const threshold = 3; // XXX hardcoded value
  //     if (items.length < threshold) {
  //       const resp = await imagesApi.getAll({ limit: threshold })
  //       items = resp.data;
  //     }
  //     items.forEach((item) => {
  //       commitAddImage(item, commit);
  //     });
  //     commit('setRecentIds', items.map((i) => i.id));
  //     // ls.set(cacheKey, true, { ttl: 60 });
  //   }
  // },
  // getNakamal: async ({ commit }, nakamalId) => {
  //   const cacheKey = `images:nakamal:${nakamalId}`;
  //   const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
  //   if (cached) {
  //     return;
  //   } else {
  //     const resp = await nakamalsApi.getImages(nakamalId);
  //     const images = resp.data;
  //     images.forEach((item) => {
  //       commitAddImage(item, commit);
  //     });
  //     // ls.set(cacheKey, true, { ttl: 300 });
  //   }
  // },
  // getUser: async ({ commit }, userId) => {
  //   const cacheKey = `images:user:${userId}`;
  //   const cached = false; // ls.get('does-not-exist'); // cacheKey - replaced to remove cache
  //   if (cached) {
  //     return;
  //   } else {
  //     const resp = await usersApi.getImages(userId);
  //     const images = resp.data;
  //     images.forEach((item) => {
  //       commitAddImage(item, commit);
  //     });
  //     // ls.set(cacheKey, true, { ttl: 300 });
  //   }
  // },
  // remove: async ({ commit, dispatch, rootState }, id) => {
  //   try {
  //     let token = rootState.auth.token;
  //     await imagesApi.remove(token, id);
  //     commit('remove', id);
  //     dispatch('notify/add', {
  //       title: i18n.t('image.alert.remove_title'),
  //       text: i18n.t('image.alert.remove_body'),
  //       type: 'warning',
  //     }, { root: true });
  //   }
  //   catch (error) {
  //     console.log('Image remove error');
  //     await dispatch('auth/checkApiError', error, { root: true });
  //   }
  // },
};

const mutations = {
  RESET (state) {
    const newState = initialState();
    Object.keys(newState).forEach(key => {
      state[key] = newState[key];
    });
  },
  ADD: (state, item) => {
    Vue.set(state.byId, item.id, item);
    if (!state.allIds.includes(item.id)) {
      state.allIds.push(item.id);
    }
    // if (!state.byNakamalId[item.nakamal]) {
    //   Vue.set(state.byNakamalId, item.nakamal, []);
    //   state.byNakamalId[item.nakamal].push(item.id);
    // }
    // else if (!state.byNakamalId[item.nakamal].includes(item.id)) {
    //   state.byNakamalId[item.nakamal].push(item.id);
    // }
  },
  // remove: (state, id) => {
  //   let index;
  //   const nId = state.byId[id].nakamal
  //   index = state.byNakamalId[nId].indexOf(id);
  //   if (index !== -1) {
  //     state.byNakamalId[nId].splice(index, 1);
  //   }
  //   index = state.recentIds.indexOf(id);
  //   if (index !== -1) {
  //     state.recentIds.splice(index, 1);
  //   }
  //   state.allIds.splice(state.allIds.indexOf(id), 1);
  //   Vue.delete(state.byId, id);
  // },
  // setRecentIds: (state, ids) => {
  //   state.recentIds = ids;
  // },
};

export default {
  actions,
  getters,
  mutations,
  namespaced: true,
  state,
};
