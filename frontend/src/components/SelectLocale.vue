<template>
  <v-menu
    left
    bottom
    offset-y
    transition="slide-x-transition"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        small
        text
        v-bind="attrs"
        v-on="on"
      >
        <v-avatar size="20" class="mr-sm-2">
          <v-img :src="selectedLanguage.flag"></v-img>
        </v-avatar>
        <span v-if="$vuetify.breakpoint.smAndUp">{{ selectedLanguage.lang }}</span>
      </v-btn>
    </template>

    <v-list>
      <v-list-item
        v-for="(item, i) in locales"
        :key="i"
        @click="selectLocale(item.locale)"
      >
        <v-list-item-icon>
          <v-avatar size="20">
            <v-img :src="item.flag"></v-img>
          </v-avatar>
        </v-list-item-icon>
        <v-list-item-title>{{ item.lang }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script>
const usaFlag = require('@/assets/usa_flag.svg');
const vuFlag = require('@/assets/vu_flag.svg');

export default {
  name: 'SelectLocale',
  data() {
    return {
      locales: [
        {
          locale: 'bi',
          lang: 'Bislama',
          flag: vuFlag,
        },
        {
          locale: 'en',
          lang: 'English',
          flag: usaFlag,
        },
      ],
    };
  },
  computed: {
    selectedLanguage() {
      const locale = this.locales.find((i) => i.locale === this.$i18n.locale);
      if (!locale) {
        return this.locales[0];
      }
      return locale;
    },
  },
  methods: {
    selectLocale(locale) {
      this.$store.dispatch('setting/setLocale', locale);
      this.$i18n.locale = locale;
    },
  },
  // created() {
  //   const locale = this.$store.getters['setting/locale'];
  //   if (locale) {
  //     console.log('lo', locale);
  //     this.selectLocale(locale);
  //   }
  // },
};
</script>
