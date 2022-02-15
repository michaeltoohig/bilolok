<template>
  <v-dialog
    v-model="show"
    max-width="500"
    scrollable
    persistent
  >
    <v-card>
      <v-card-title>Start Compass Mode?</v-card-title>
      <v-card-text>
        <div class="d-flex flex-row justify-start align-center">
          <v-icon class="mr-3" size="64">mdi-compass</v-icon>
          The compass uses your device's GPS to guide you to the kava bar.
          This feature is still experimental so have patience if it does not
          work perfectly yet. Your device's GPS will also affect the performance.
        </div>
        <v-alert
          elevation="2"
          color="info"
          icon="mdi-run-fast"
          class="mt-3"
        >
          For best accuracy you must be moving (e.g. walking) so we can
          point you in the correct direction.
        </v-alert>
        <v-list dense>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-up</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Up Arrow</v-list-item-title>
              <v-list-item-subtitle>
                The kava bar is ahead of you
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-down</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Down Arrow</v-list-item-title>
              <v-list-item-subtitle>
                Turn around the kava bar is somewhere behind you
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-left</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Left Arrow</v-list-item-title>
              <v-list-item-subtitle>The kava bar is to your left</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-right</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>Right Arrow</v-list-item-title>
              <v-list-item-subtitle>The kava bar is to your right</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          outlined
          @click="hide"
        >
          Cancel
        </v-btn>
        <v-btn
          text
          outlined
          @click="setStartCompassMode"
        >
          Start
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'CompassModeIntroDialog',
  props: ['show'],
  methods: {
    ...mapActions(
      'map', [
        'startCompassMode',
      ],
    ),
    hide() {
      this.$emit('hide');
    },
    setStartCompassMode() {
      this.hide();
      this.startCompassMode();
    },
  },
};
</script>

<style>

</style>
