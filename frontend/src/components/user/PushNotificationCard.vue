<template>
  <v-card>
    <v-card-text>
      <v-card-title>Push Notifications</v-card-title>
      <v-card-subtitle>Experimental Feature: {{ isSubscribed ? 'ON' : 'OFF' }}</v-card-subtitle>
      <v-btn
        @click="togglePushNotifications"
        outlined
        block
      >{{ notificationsEnabled ? 'Disable' : 'Allow' }} Notifications</v-btn>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import subscriptionApi from '@/api/subscriptions';
import deviceId from '@/deviceId';

export default {
  name: 'PushNotificationCard',
  data() {
    return {
      subscription: null,

      notificationsSupported: false,
      publicKey: null,
      serviceWorkerRegistation: null,
      isSubscribed: false,
    };
  },
  computed: {
    notificationsEnabled() {
      return this.isSubscribed;
    },
    ...mapGetters({
      me: 'auth/user',
      token: 'auth/token',
    }),
  },
  methods: {
    async postSubscription(subscription) {
      const data = {
        subscription_info: subscription,
        device_id: deviceId,
        user_agent: navigator.userAgent,
      };
      await subscriptionApi.create(this.token, data);
      this.subscription = subscription;
      this.isSubscribed = true;
    },
    async deleteSubscription() {
      await subscriptionApi.remove(this.token, deviceId);
      if (this.subscription !== null) {
        this.subscription.unsubscribe();
        this.subscription = null;
      }
      this.isSubscribed = false;
    },
    async togglePushNotifications() {
      if (this.notificationsSupported) {
        // Find out if we need to create a subscription or delete it
        if (!this.notificationsEnabled) {
          // Ask permission and when granted, create new subscription
          Notification.requestPermission()
            .then((result) => {
              // if granted, create new subscription
              if (result === 'granted') {
                this.createSubscription()
                  .then((subscription) => {
                    console.log('subscription created on the client', subscription);
                    this.postSubscription(subscription);
                  });
              } else {
                console.log('User did not granted permission');
              }
            });
        } else {
          this.deleteSubscription();
        }
      }
    },
    createSubscription() {
      console.log('ask for active service worker registration');
      if (this.serviceWorkerRegistation === null) {
        return navigator.serviceWorker.ready // returns a Promise, the active SW registration
          .then((swreg) => {
            this.serviceWorkerRegistation = swreg;
            return this.subscribe();
          });
      }
      return this.subscribe();
    },
    subscribe() {
      console.log('create new subscription for this browser on this device');
      // create new subscription for this browser on this device
      const convertedVapidPublicKey = this.urlB64ToUint8Array(this.publicKey);
      // return the subscription promise, we chain another then where we can send it to the server
      return this.serviceWorkerRegistation.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: convertedVapidPublicKey,
      });
    },
    urlB64ToUint8Array(base64String) {
      const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
      const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
      const rawData = window.atob(base64);
      const outputArray = new Uint8Array(rawData.length);
      for (let i = 0; i < rawData.length; i += 1) {
        outputArray[i] = rawData.charCodeAt(i);
      }
      return outputArray;
    },
  },
  async created() {
    // Fetch VAPID public key from backend if push notifications are supported on this device
    if ('Notification' in window && 'serviceWorker' in navigator) {
      this.notificationsSupported = true;
      const resp = await subscriptionApi.getPublicKey(this.token);
      this.publicKey = resp.data.public_key;
    }
  },
  mounted() {
    if (!this.notificationsSupported) return;
    // Find out if the user has a subscription at the moment.
    // If so, send to backend
    navigator.serviceWorker.ready
      .then((swReg) => {
        this.serviceWorkerRegistation = swReg;
        return this.serviceWorkerRegistation.pushManager.getSubscription();
      })
      .then((subscription) => {
        this.isSubscribed = !(subscription === null);
        if (this.isSubscribed) {
          console.log('User is subscribed');
          this.postSubscription(subscription);
        } else {
          console.log('User is not subscribed');
        }
      });
  },
};
</script>

<style>

</style>
