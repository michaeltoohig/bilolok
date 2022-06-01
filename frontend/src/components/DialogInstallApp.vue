<template>
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
</template>

<script>
export default {
  name: 'DialogInstallApp',
  data() {
    return {
      deferredPrompt: null,
      showInstallPrompt: false,
      blockInstallPrompt: false,
    };
  },
  methods: {
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
  created() {
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
  },
};
</script>

<style>

</style>