/* This mixin adds:
 * - `isOnline`, `isOffline` data properties
 * - `online`, `offline` in-component events
 */
export default {
  data() {
    return {
      isOnline: false,
      isOffline: false,
    };
  },
  mounted() {
    if (typeof window !== 'undefined') {
      // eslint-disable-next-line
      navigator.onLine ? this.isOnline = true : this.isOffline = true;

      const onlineHandler = () => {
        this.$emit('online');
        this.isOnline = true;
        this.isOffline = false;
      };

      const offlineHandler = () => {
        this.$emit('offline');
        this.isOffline = true;
        this.isOnline = false;
      };

      window.addEventListener('online', onlineHandler);
      window.addEventListener('offline', offlineHandler);

      this.$once('hook:beforeDestroy', () => {
        window.removeEventListener('online', onlineHandler);
        window.removeEventListener('offline', offlineHandler);
      });
    }
  },
};
