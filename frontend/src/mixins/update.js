/* This mixin adds:
 * - `noServiceWorker`, `refreshing`, `registartion`, `updateExists` data properties
 * - `updateAvailable`, `refreshApp` methods
 */
export default {
  data() {
    return {
      noServiceWorker: false,
      refreshing: false,
      registration: null,
      updateExists: false,
    };
  },
  created() {
    if (!('serviceWorker' in navigator)) {
      console.log('No service worker available :(');
      this.noServiceWorker = true;
      return;
    }

    // once means the listener is removed after being called
    document.addEventListener('swUpdated', this.updateAvailable, { once: true });

    // Prevent multiple refreshes
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      // We'll also need to add 'refreshing' to our data originally set to false.
      if (this.refreshing) return;
      this.refreshing = true;
      // Here the actual reload of the page occurs
      window.location.reload();
    });
  },
  methods: {
    // Store the SW registration so we can send it a message
    // We use `updateExists` to control whatever alert, toast, dialog, etc we want to use
    // To alert the user there is an update they need to refresh for
    updateAvailable(event) {
      this.registration = event.detail;
      this.updateExists = true;
    },

    // Called when the user accepts the update
    refreshApp() {
      console.log('refreshing app');
      this.updateExists = false;
      // Make sure we only send a 'skip waiting' message if the SW is waiting
      if (!this.registration || !this.registration.waiting) return;
      // Send message to SW to skip the waiting and activate the new SW
      this.registration.waiting.postMessage({ type: 'SKIP_WAITING' });
    },
  },
};
