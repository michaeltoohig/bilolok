<template>
  <l-control
    :position="'topright'"
  >
    <v-card
      v-show="showCompass"
      max-width="200"
      outlined
      style="opacity: 80%;"
    >
      <v-progress-linear
        v-show="!user"
        color="primary"
        indeterminate
        absolute
        top
        height="6"
      ></v-progress-linear>
      <v-card-text v-if="user">
        <v-alert color="warning" v-if="!user.heading">
          Your device did not provide the direction you are facing
          so we can not show you the compass. Usually, mobile devices
          provide a heading but some devices do not.
        </v-alert>
        <span class="small">Heading To:</span>
        <h3>{{ nakamal.name }}</h3>
        <div class="d-flex justify-center align-center">
          <v-icon size="144">{{ bearingIcon }}</v-icon>
        </div>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          text
          outlined
          @click="setShowCompass(false)"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </l-control>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { LControl } from 'vue2-leaflet';

export default {
  name: 'Compass',
  components: {
    LControl,
  },
  computed: {
    ...mapGetters({
      showCompass: 'map/showCompass',
      user: 'map/location',
      nakamal: 'nakamal/selected',
    }),
    bearing() {
      if (!this.user || !this.user.heading || !this.nakamal) {
        return null;
      }
      const startLat = this.toRadians(this.user.latitude);
      const startLng = this.toRadians(this.user.longitude);
      const destLat = this.toRadians(this.nakamal.lat);
      const destLng = this.toRadians(this.nakamal.lng);

      const y = Math.sin(destLng - startLng) * Math.cos(destLat);
      const x = Math.cos(startLat) * Math.sin(destLat)
        - Math.sin(startLat) * Math.cos(destLat) * Math.cos(destLng - startLng);
      let brng = Math.atan2(y, x);
      brng = this.toDegrees(brng);
      return (brng + 360 - this.user.heading) % 360;
    },
    bearingIcon() {
      let icon = 'mdi-crosshairs-question';
      if (this.bearing === null) {
        return icon;
      }
      if (this.bearing > 337.5 || this.bearing < 22.5) {
        icon = 'mdi-arrow-up';
      } else if (this.bearing > 22.5 && this.bearing < 67.5) {
        icon = 'mdi-arrow-top-right';
      } else if (this.bearing > 67.5 && this.bearing < 112.5) {
        icon = 'mdi-arrow-right';
      } else if (this.bearing > 112.5 && this.bearing < 157.5) {
        icon = 'mdi-arrow-bottom-right';
      } else if (this.bearing > 157.5 && this.bearing < 202.5) {
        icon = 'mdi-arrow-down';
      } else if (this.bearing > 202.5 && this.bearing < 247.5) {
        icon = 'mdi-arrow-bottom-left';
      } else if (this.bearing > 247.5 && this.bearing < 292.5) {
        icon = 'mdi-arrow-left';
      } else if (this.bearing > 292.5 && this.bearing < 337.5) {
        icon = 'mdi-arrow-top-left';
      }
      return icon;
    },
  },
  methods: {
    ...mapActions(
      'map', [
        'setShowCompass',
      ],
    ),
    toRadians(deg) {
      return (deg * Math.PI) / 180;
    },
    toDegrees(rad) {
      return (rad * 180) / Math.PI;
    },
  },
};
</script>

<style>

</style>
