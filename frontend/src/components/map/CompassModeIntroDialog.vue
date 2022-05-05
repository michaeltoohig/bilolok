<template>
  <v-dialog
    v-model="show"
    max-width="500"
    scrollable
    persistent
  >
    <v-card>
      <v-card-title>{{ $t('map.compass.start_compass_mode') }}?</v-card-title>
      <v-card-text>
        <div class="d-flex flex-row justify-start align-center">
          <v-icon class="mr-3" size="64">mdi-compass</v-icon>
          {{ $t('map.compass.gps_explanation') }}
        </div>
        <v-alert
          elevation="2"
          color="info"
          icon="mdi-run-fast"
          class="mt-3"
        >
          {{ $t('map.compass.gps_explanation_extra') }}
        </v-alert>
        <v-list dense>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-up</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ $t('map.compass.arrow_up') }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ $t('map.compass.arrow_up_explanation') }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-down</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ $t('map.compass.arrow_down') }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ $t('map.compass.arrow_down_explanation') }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-left</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ $t('map.compass.arrow_left') }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ $t('map.compass.arrow_left_explanation') }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item two-line>
            <v-list-item-icon>
              <v-icon>mdi-arrow-right</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>{{ $t('map.compass.arrow_right') }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ $t('map.compass.arrow_right_explanation') }}
              </v-list-item-subtitle>
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
          {{ $t('buttons.cancel') }}
        </v-btn>
        <v-btn
          text
          outlined
          @click="setStartCompassMode"
        >
          {{ $t('buttons.start') }}
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
