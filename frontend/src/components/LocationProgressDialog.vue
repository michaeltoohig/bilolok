<template>
  <v-dialog
      v-model="show"
      max-width="500"
      persistent
    >
      <v-card>
        <v-progress-linear
          color="primary"
          indeterminate
          absolute
          top
          height="6"
        ></v-progress-linear>
        <v-card-title>Getting Your Location</v-card-title>
        <v-card-text>
          <div class="d-flex flex-row justify-start align-center">
            <v-icon class="mr-3" size="64">mdi-crosshairs-gps</v-icon>
            Please wait while we get your device's location. This may take a few seconds.
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'LocationProgressDialog',
  computed: {
    ...mapGetters({
      show: 'map/showLocationProgress',
    }),
  },
};
</script>

<style>

</style>
