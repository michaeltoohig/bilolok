<template>
  <v-dialog
    v-model="dialog"
    persistent
    max-width="600px"
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
        <span class="headline">No Network Connection</span>
      </v-card-title>
      <v-card-text>
        <p>
          You are currently offline. The app is made so that
          the map should continue to work in areas you've
          already visited.
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
