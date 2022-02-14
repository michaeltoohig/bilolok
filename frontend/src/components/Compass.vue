<template>

  <v-card
    v-show="compassMode"
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
        Your device did not provide your heading so we can not
        point you towards the kava bar.
      </v-alert>
      <span class="small">Heading To:</span>
      <h3>{{ nakamal.name }}</h3>
      <div class="d-flex justify-center align-center">
        <v-icon size="144">{{ bearingIcon }}</v-icon>
      </div>
      <h5>Distance: {{ displayDistance }}</h5>
      <h5>Trip: {{ displayTrip }}</h5>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-btn
        v-show="showFinishBtn"
        color="primary"
        @click="saveTrip"
      >
        Finish!
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        text
        outlined
        :disabled="showFinishBtn"
        @click="stopCompassMode"
      >
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import { latLng } from 'leaflet';

export default {
  name: 'Compass',
  computed: {
    ...mapGetters({
      isUserVerified: 'auth/isUserVerified',
      compassMode: 'map/compassMode',
      compassModePolyline: 'map/compassModePolyline',
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
    showFinishBtn() {
      return this.distance <= 30; // XXX hardcoded value
    },
    distance() {
      if (!this.user || !this.nakamal) return null;
      const userLatLng = latLng(this.user.latitude, this.user.longitude);
      return Math.round(userLatLng.distanceTo(this.nakamal.latLng));
    },
    displayDistance() {
      let dist = this.distance;
      if (dist < 1000) {
        dist = `${dist} meters`;
      } else {
        dist = (dist / 1000).toFixed(1);
        dist = `${dist} kilometers`;
      }
      return dist;
    },
    displayTrip() {
      if (this.compassModePolyline.length === 0) return 0;
      let prevPoint = null;
      let distance = 0;
      this.compassModePolyline.forEach((p) => {
        if (prevPoint !== null) {
          distance += Math.round(latLng(prevPoint).distanceTo(latLng(p)));
        }
        prevPoint = p;
      });
      if (distance < 1000) {
        distance = `${distance} meters`;
      } else {
        distance = (distance / 1000).toFixed(1);
        distance = `${distance} kilometers`;
      }
      return distance;
    },
  },
  methods: {
    // ...mapActions(
    //   'map', [
    //     'stopCompassMode',
    //   ],
    // ),
    saveTrip() {
      console.log('TODO save trip info, play sound, etc.');
      if (this.isUserVerified) {
        console.log('TODO save trip info');
        this.$store.dispatch('notify/add', {
          title: 'Trip Complete',
          text: 'You have arrived at your destination. You should now check-in to the kava bar.',
          color: 'primary',
          duration: 5_000,
        });
      } else {
        this.$store.dispatch('notify/add', {
          title: 'Trip Not Saved',
          text: 'You have not verified your email yet. We did not save your trip and you will not be able to check-in to the kava bar.',
          color: 'warning',
          duration: 5_000,
        });
      }
      this.stopCompassMode();
      setTimeout(() => {
        this.$router.push({ name: 'Nakamal', params: { id: this.nakamal.id } });
      }, 1000);
    },
    stopCompassMode() {
      this.$emit('stop');
    },
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
