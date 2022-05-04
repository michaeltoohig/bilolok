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
      <SideBar></SideBar>
      <v-main>
        <div
          style="position: fixed; z-index: 3001; width: 100%;"
        >
          <v-row class="mt-2 mx-0">
            <v-col justify="center">
              <v-alert
                v-if="noServiceWorker"
                class="mx-auto"
                max-width="600"
                type="warning"
                dark
                :prominent="!$vuetify.breakpoint.xsOnly"
                transition="scale-transition"
                dismissible
              >
                <div class="title">
                  {{ $t('app.no_service_worker_title') }}
                </div>
                <div v-html="$t('app.no_service_worker_body')" />
              </v-alert>
              <v-alert
                v-if="updateExists"
                class="mx-auto"
                max-width="450"
                type="info"
                dark
                :prominent="!$vuetify.breakpoint.xsOnly"
                transition="scale-transition"
              >
                <v-row align="center">
                  <v-col class="grow">
                    {{ $t('app.update_available_title') }}
                  </v-col>
                  <v-col class="shrink">
                    <v-btn @click="refreshApp">{{ $t('app.update_available_btn') }}</v-btn>
                  </v-col>
                </v-row>
              </v-alert>
            </v-col>
          </v-row>
        </div>
        <router-view></router-view>
      </v-main>
      <Notifications></Notifications>

      <v-dialog
        v-model="showAuthModal"
        persistent
        max-width="400"
      >
        <v-card>
          <v-card-title>{{ $t('auth.alert.auth_required_title') }}</v-card-title>
          <v-card-subtitle>
            {{ $t('auth.alert.auth_required_subtitle') }}
          </v-card-subtitle>
          <v-card-text>
            <p>{{ $t('auth.alert.auth_required_body') }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              outlined
              @click="goToLogin"
            >
              {{ $t('auth.login') }}
            </v-btn>
            <v-btn
              text
              outlined
              @click="goToSignup"
            >
              {{ $t('auth.register') }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn text @click="closeAuthModal">
              {{ $t('buttons.close') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showUserVerifiedModal"
        persistent
        max-width="400"
      >
        <v-card>
          <v-card-title>{{ $t('auth.alert.email_verification_required_title') }}</v-card-title>
          <v-card-subtitle>
            {{ $t('auth.alert.email_verification_required_subtitle') }}
          </v-card-subtitle>
          <div class="d-flex justify-center">
            <v-icon size="100">mdi-email-alert</v-icon>
          </div>
          <v-card-text>
            <p>{{ $t('auth.alert.email_verification_required_body') }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="closeUserVerifiedModal">
              {{ $t('buttons.close') }}
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn
              text
              outlined
              color="primary"
              @click="sendVerificationEmail"
            >
              {{ $t('auth.send_verification_email') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

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
              {{ $t('buttons.cancel') }}
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
import UpdateMixin from './mixins/update';
import Notifications from './components/Notifications.vue';
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
  },
  mixins: [UpdateMixin, OfflineMixin],
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
      showAuthModal: 'auth/showAuthModal',
      showUserVerifiedModal: 'auth/showUserVerifiedModal',
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
    closeAuthModal() {
      this.$store.dispatch('auth/setShowAuthModal', false);
    },
    closeUserVerifiedModal() {
      this.$store.dispatch('auth/setShowUserVerifiedModal', false);
    },
    goToLogin() {
      this.closeAuthModal();
      this.$router.push({ name: 'Auth', params: { auth: 'login' } });
    },
    goToSignup() {
      this.closeAuthModal();
      this.$router.push({ name: 'Auth', params: { auth: 'signup' } });
    },
    sendVerificationEmail() {
      this.$store.dispatch('auth/requestVerification');
    },
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
