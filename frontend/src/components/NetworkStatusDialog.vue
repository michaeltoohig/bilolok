<template>
  <v-dialog
    v-model="dialog"
    persistent
    max-width="500px"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-fab-transition>
        <v-btn
          v-show="isOffline"
          color="danger"
          fab
          dark
          v-bind="attrs"
          v-on="on"
        >
          <v-icon>mdi-wifi-strength-alert-outline</v-icon>
        </v-btn>
      </v-fab-transition>
    </template>
    <v-card>
      <v-card-title>
        <v-icon class="mr-2">mdi-wifi-strength-alert-outline</v-icon>
        You Are Offline
      </v-card-title>
      <v-card-text>
        <p>
          You are currently offline. The app will continue to
          work with data you have already downloaded previously.
          Trying to view the map in areas you have not browsed
          recently will fail. We are working on adding more offline
          functionality in the future to improve offline experience.
        </p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          text
          @click="dialog = false"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import OfflineMixin from '@/mixins/offline';

export default {
  name: 'NetworkStatusSystemBar',
  mixins: [OfflineMixin],
  data() {
    return {
      dialog: false,
    };
  },
};
</script>

<style>

</style>
