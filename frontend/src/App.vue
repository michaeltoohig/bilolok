<template>
  <v-app>
    <v-main v-if="loggedIn===null">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">Loading...</div>
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
          style="position: absolute; z-index: 3001; width: 100%;"
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
                  Some Features Not Available.
                </div>
                <div>
                  Your browser does not support
                  <a
                    target="_blank"
                    href="https://developers.google.com/web/fundamentals/primers/service-workers"
                  >Service Workers</a>
                  so many features of this app will not work as
                  intended and it will be slower.
                  Please consider using a more modern
                  web browser.
                </div>
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
                    New Updates Available.
                  </v-col>
                  <v-col class="shrink">
                    <v-btn @click="refreshApp">Update Now!</v-btn>
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
          <v-card-title>Login Required</v-card-title>
          <v-card-subtitle>You must be logged in to perform that action.</v-card-subtitle>
          <v-card-text>
            <p>
              We require users have an account with us to perform some actions.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-btn
              text
              outlined
              @click="goToLogin"
            >Login</v-btn>
            <v-btn
              text
              outlined
              @click="goToSignup"
            >Register</v-btn>
            <v-spacer></v-spacer>
            <v-btn text @click="closeAuthModal">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="showUserVerifiedModal"
        persistent
        max-width="400"
      >
        <v-card>
          <v-card-title>Email Verification Required</v-card-title>
          <v-card-subtitle>You must verify your email to perform that action.</v-card-subtitle>
          <v-card-text>
            <p>
            To prevent abuse we require a user verify the email address they
            provided during sign up. Look in your email for a messag from
            Bilolok and a link to verify your email will be inside that email.
            </p>
            <p>
            Then, you may try again.
            </p>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="closeUserVerifiedModal">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </v-app>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import Notifications from './components/Notifications.vue';
import SideBar from './components/SideBar.vue';
import update from './mixins/update';

export default {
  name: 'App',
  components: {
    SideBar,
    Notifications,
  },
  mixins: [update],
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
    // setShowUserVerifiedModal() {
    //   console.log('yyy');
    //   this.showUserVerifiedModal = true;
    // },
  },
  async created() {
    // this.$on('showUserVerifiedModal', this.setShowUserVerifiedModal);
    await this.checkLoggedIn();
    if (process.browser) {
      this.$store.dispatch('setting/checkDarkMode');
    }
  },
};
</script>
