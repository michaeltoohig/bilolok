<template>
  <v-app>
    <v-system-bar
      app
      fixed
      height="30"
      color="primary"
      v-if="isOffline"
      dark
    >
      <span class="mx-auto">
      <v-icon>mdi-wifi-strength-alert-outline</v-icon>
        {{ $t('app.offline') }}
      </span>
    </v-system-bar>

    <v-main v-if="loggedIn===null">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">{{ $t('loading.app') }}</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </v-main>

    <div v-else>
      <AlertUpdateAvailable/>
      <SideBar></SideBar>
      <v-main>
        <router-view></router-view>
      </v-main>
      <Notifications></Notifications>

      <DialogUserAuthRequired />

      <DialogInstallApp />
    </div>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import OfflineMixin from '@/mixins/offline';
import Notifications from '@/components/Notifications.vue';
import AlertUpdateAvailable from '@/components/AlertUpdateAvailable.vue';
import DialogUserAuthRequired from '@/components/DialogUserAuthRequired.vue';
import DialogInstallApp from '@/components/DialogInstallApp.vue';
import SideBar from './components/SideBar.vue';

export default {
  name: 'App',
  metaInfo: {
    title: 'Bilolok | it means kava',
    meta: [
      {
        property: 'og:title',
        content: 'Bilolok | it means kava',
        vmid: 'og:title',
      },
      {
        property: 'og:description',
        content: 'Bilolok is an app for kava bars and kava drinkers in Port Vila, Vanuatu.',
        vmid: 'og:description',
      },
      {
        property: 'og:url',
        content: 'https://bilolok.com',
        vmid: 'og:url',
      },
      {
        property: 'og:image',
        content: 'https://bilolok.com/img/cover.jpg',
        vmid: 'og:image',
      },
      {
        property: 'og:image:type',
        content: 'image/png',
        vmid: 'og:image:type',
      },
      {
        property: 'og:image:width',
        content: '1448',
        vmid: 'og:image:width',
      },
      {
        property: 'og:image:height',
        content: '636',
        vmid: 'og:image:height',
      },
    ],
  },
  components: {
    SideBar,
    Notifications,
    AlertUpdateAvailable,
    DialogUserAuthRequired,
    DialogInstallApp,
  },
  mixins: [OfflineMixin],
  computed: {
    ...mapGetters({
      loggedIn: 'auth/isLoggedIn',
      darkMode: 'setting/darkMode',
    }),
  },
  watch: {
    // This may be a less performant solution to update theme
    darkMode(value) {
      this.$vuetify.theme.dark = value;
    },
  },
  methods: {
    ...mapActions({
      checkLoggedIn: 'auth/checkLoggedIn',
    }),
  },
  async created() {
    if (process.browser) {
      this.$store.dispatch('setting/checkDarkMode');
      this.$store.dispatch('setting/checkLocale');
    }
    // Lastly, check user auth status which will remove the loading screen
    await this.checkLoggedIn();
  },
};
</script>

<style>
/* See bug report here https://github.com/vuetifyjs/vuetify/issues/9130 */
.v-card__text, .v-card__title {
  word-break: normal !important;
}
</style>
