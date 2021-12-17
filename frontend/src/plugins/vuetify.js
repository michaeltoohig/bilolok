/* eslint-disable */

import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import colors from 'vuetify/lib/util/colors';

const porsche = '#E5A55B';
const palmLeaf = '#16240A';
const christi = '#29AD08';
const slateGrey = '#727F8D';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
    //   dark: {
    //     primary: porsche,
    //     secondary: slateGrey,
    //     accent: christi,
    //     success: palmLeaf,
    //     info: christi,
    //   },
    //   light: {
    //     primary: porsche,
    //     secondary: slateGrey,
    //     accent: christi,
    //     success: palmLeaf,
    //     info: christi,
    //   },
      light: {
        primary: colors.brown.darken1,
        secondary: colors.brown.lighten4,
        accent: colors.orange.darken4,
        error: colors.orange.darken1,
        info: colors.purple.darken3,
        success: colors.green.darken4,
        warning: colors.deepOrange.darken2,
      },
    },
  },
});
