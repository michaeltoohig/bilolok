<template>
  <v-fab-transition>
    <v-btn
      v-if="showNewNakamalMarker"
      color="accent"
      dark
      fab
      @click="setShowNewNakamalMarker(false)"
    >
      <v-icon>mdi-close</v-icon>
    </v-btn>
    <v-speed-dial
      v-else
      v-model="fab"
      transition="slide-y-reverse-transition"
    >
      <template v-slot:activator>
        <v-btn
          v-model="fab"
          color="secondary darken-2"
          dark
          fab
        >
          <v-icon v-if="fab">
            mdi-close
          </v-icon>
          <v-icon v-else>
            mdi-menu
          </v-icon>
        </v-btn>
      </template>
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            small
            color="secondary darken-1"
            @click.stop="getLocation"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-crosshairs-gps</v-icon>
          </v-btn>
        </template>
        <span>Get Location</span>
      </v-tooltip>
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            small
            color="secondary darken-1"
            @click.stop="setShowSearch(true)"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-map-search</v-icon>
          </v-btn>
        </template>
        <span>Search</span>
      </v-tooltip>
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            small
            color="secondary darken-1"
            :disabled="false"
            @click.stop="setShowHeatmapMenu(true)"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-fire</v-icon>
          </v-btn>
        </template>
        <span>Check-in Heatmap (Needs Repair)</span>
      </v-tooltip>
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            small
            color="secondary darken-1"
            @click.stop="setShowFilters(true)"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-menu-open</v-icon>
          </v-btn>
        </template>
        <span>Filter</span>
      </v-tooltip>
      <v-tooltip left>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            fab
            dark
            small
            color="secondary darken-1"
            @click.stop="newNakamalMarker"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon>mdi-map-marker-plus</v-icon>
          </v-btn>
        </template>
        <span>Add Kava Bar</span>
      </v-tooltip>
    </v-speed-dial>
  </v-fab-transition>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import { latLng } from 'leaflet';

export default {
  name: 'NakamalMapFabButtons',
  data() {
    return {
      fab: false,
    };
  },
  computed: {
    ...mapGetters({
      isUserVerified: 'auth/isUserVerified',
      showNewNakamalMarker: 'map/showNewNakamalMarker',
      showHeatmap: 'map/showHeatmap',
      hasFilters: 'nakamal/hasFilters',
    }),
  },
  methods: {
    // Location-based methods feel a bit out of place here.
    // Perhaps better suited if in the map store.
    getLocationSuccess(pos, result) {
      this.setShowLocationProgress(false);
      if (result === 'success') {
        this.setLocation(pos.coords);
        // next line may fail when I get to test it on a mobile device
        this.$root.$emit('fly-to', latLng(pos.coords.latitude, pos.coords.longitude));
      } else {
        this.getLocationError({});
      }
    },
    getLocationError(error) {
      console.log('Location error:', error);
      this.setShowLocationProgress(false);
      this.$store.dispatch('notify/add', {
        title: 'Location Not Found',
        text: 'Your device did not provide an accurate location.',
        color: 'error',
        duration: 5_000,
      });
    },
    getLocationProgress(pos) {
      console.log('position progress', pos);
      this.setShowLocationProgress(true);
    },
    getLocation() {
      this.$root.$emit('fly-to', latLng(-17.4, 168.4));
      if (!('geolocation' in navigator)) {
        this.$store.dispatch('notify/add', {
          title: 'Location Not Available',
          text: 'Your device does not provide location or you have blocked location access.',
          color: 'info',
          duration: 5_000,
        });
        return;
      }
      // get position
      this.setShowLocationProgress(true);
      navigator.geolocation.getAccurateCurrentPosition(
        this.getLocationSuccess,
        this.getLocationError,
        this.getLocationProgress,
        {
          desiredAccuracy: 20,
          desiredAccuracyCountMin: 2,
          maxWait: 15000,
        },
      );
    },
    ...mapActions(
      'nakamal', [
        'removeFilters',
      ],
    ),
    ...mapActions(
      'map', [
        'setLocation',
        'setShowLocationProgress',
        'startCompassMode',
        'stopCompassMode',
        'setBounds',
        'setCenter',
        'setZoom',
        'setShowNewNakamalMarker',
        'setShowFilters',
        'setShowDetails',
        'setShowSearch',
        'setShowHeatmapMenu',
        'setShowHeatmap',
      ],
    ),
    newNakamalMarker() {
      this.fab = false;
      if (this.isUserVerified) {
        this.setShowNewNakamalMarker(true);
        if (this.hasFilters) {
          this.removeFilters();
          this.$store.dispatch('notify/add', {
            title: 'Filters Removed',
            text: 'We removed filters so you do not accidentally add an existing kava bar.',
            color: 'info',
            duration: 5_000,
          });
        }
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
  },
};
</script>

<style>

</style>
