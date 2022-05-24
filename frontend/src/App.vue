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

      <v-dialog
        v-model="showInstallPrompt"
        persistent
        max-width="400"
        transition="dialog-top-transition"
      >
        <v-card>
          <v-card-title>{{ $t('app.install_app_title') }}</v-card-title>
          <v-card-subtitle>{{ $t('app.install_app_subtitle') }}</v-card-subtitle>
          <v-card-text>
            <p>{{ $t('app.install_app_body') }}</p>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-spacer></v-spacer>
            <v-btn
              text
              @click="showInstallPrompt = false"
            >
              {{ $t('buttons.close') }}
            </v-btn>
            <v-btn
              text
              outlined
              color="primary"
              @click="installApp"
            >
              {{ $t('app.install_app_btn') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import OfflineMixin from '@/mixins/offline';
import Notifications from '@/components/Notifications.vue';
import AlertUpdateAvailable from '@/components/AlertUpdateAvailable.vue';
import DialogUserAuthRequired from '@/components/DialogUserAuthRequired.vue';
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
  },
  mixins: [OfflineMixin],
  data() {
    return {
      deferredPrompt: null,
      showInstallPrompt: false,
      blockInstallPrompt: false,
    };
  },
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
    async installApp() {
      // hide our install prompt
      this.showInstallPrompt = false;
      // show device's install prompt
      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      console.log('install outcome:', outcome);
      // prevent install prompt from activating again for at least this session
      this.blockInstallPrompt = true;
      // TODO act on user outcome
      this.deferredPrompt = null;
    },
  },
  async created() {
    if (process.browser) {
      this.$store.dispatch('setting/checkDarkMode');
      this.$store.dispatch('setting/checkLocale');
    }
    // Save prompt to allow user to install app to their phone
    window.addEventListener('beforeinstallprompt', (e) => {
      console.log('beforeinstallprompt');
      // prevent browser from showing the prompt and hold it for later
      e.preventDefault();
      this.deferredPrompt = e;
      // show the prompt if user remains on site for extended period
      if (!this.blockInstallPrompt) {
        setTimeout(() => {
          this.showInstallPrompt = true;
        }, 1000 * 60);
      }
      return false;
    });

    // Add event listener to know when user installs app.
    //  Could be used to modify design, log event, etc
    window.addEventListener('appinstalled', () => {
      // TODO show always persistent install now option in UI
      //   then we can remove that if this event occurs.
      // Possibly, only show to mobile devices in browsers.
      this.showInstallPrompt = false;
      this.blockInstallPrompt = true;

      // Clear the deferredPrompt so it can be garbage collected
      this.deferredPrompt = null;
      // Optionally, send analytics event to indicate successful install
      console.log('PWA was installed');
    });

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
