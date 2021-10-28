import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

import colors from 'vuetify/lib/util/colors';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
    options: {
      customProperties: true,
    },
    themes: {
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
