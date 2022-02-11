/* eslint-disable */

<template>
  <v-container
    fluid
    id="map-wrapper"
    :class="isOffline ? 'map-offline' : 'map-online'"
    class="pa-0"
  >
    <v-progress-linear
      :active="mapLoading"
      v-model="tilesLoadingPercent"
      color="primary"
      absolute
      top
    ></v-progress-linear>

    <l-map
      style="z-index: 0;"
      ref="map"
      :zoom="zoom"
      :center="center"
      :bounds="bounds"
      :max-bounds="maxBounds"
      :min-zoom="minZoom"
      :options="mapOptions"
      @update:bounds="setBounds"
      @update:center="setCenter"
      @update:zoom="setZoom"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
        @tileloadstart="mapTileLoading += 1"
        @tileload="mapTileLoaded += 1"
        @loading="mapLoading = true"
        @load="tileLoadComplete"
      />

      <NewNakamalDialog
        :show="showNewNakamalMarker"
      ></NewNakamalDialog>

      <v-dialog
        v-model="showNearbyNakamals"
        persistent
        scrollable
        width="500"
      >
        <v-card>
          <v-card-title >
            Nearby Kava Bars
          </v-card-title>
          <v-divider></v-divider>
          <v-card-text v-if="nearbyNakamals.length > 0">
            <v-row dense>
              <v-col cols="12" v-for="nakamal in nearbyNakamals" :key="nakamal.id">
                <NakamalListItem
                  :nakamal="nakamal"
                  v-on:fly-to-nearby="flyToNearby"
                ></NakamalListItem>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-text v-else class="text-center mt-5 font-weight-bold h5">
            No kava bars nearby...
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              text
              @click="showNearbyNakamals = false"
            >
              close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <l-marker
        v-if="location"
        :icon="iconGeolocation"
        :lat-lng="[location.latitude, location.longitude]"
        @click="showNearbyNakamals = true;"
      ></l-marker>

      <l-marker
        v-for="nakamal in nakamals"
        :key="nakamal.id"
        :icon="iconMarker(nakamal.id)"
        :lat-lng="nakamal.latLng"
        @click="markerClick(nakamal.id)"
      ></l-marker>

      <l-layer-group v-if="selectedNakamal" ref="nakamalPopup">
        <NakamalMapPopup></NakamalMapPopup>
      </l-layer-group>

      <l-control
        :position="'bottomleft'"
      >
        <NetworkStatusDialog></NetworkStatusDialog>
      </l-control>

      <l-control
        :position="'bottomright'"
      >
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
                  @click.stop="toggleCheckinHeatmap"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon>mdi-map-check</v-icon>
                </v-btn>
              </template>
              <span>Check-in Heatmap</span>
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
                  <v-icon>mdi-map-minus</v-icon>
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
      </l-control>

      <Vue2LeafletHeatmap
        :visible="showHeatmap"
        :lat-lng="checkinHeatmap"
        :radius="20"
        :min-opacity=".50"
        :max-zoom="16"
        :blur="18"
      ></Vue2LeafletHeatmap>
    </l-map>

    <NakamalSearchDialog></NakamalSearchDialog>

    <NakamalBottomSheet></NakamalBottomSheet>

    <NakamalFilterSidebar></NakamalFilterSidebar>

    <v-dialog
      v-model="showLocationProgress"
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
  </v-container>
</template>

<script>
import OfflineMixin from '@/mixins/offline';
import {
  mapActions,
  mapGetters,
} from 'vuex';
import {
  icon, latLngBounds,
} from 'leaflet';
import {
  LMap, LTileLayer, LMarker, LControl, LLayerGroup,
} from 'vue2-leaflet';
import sphereKnn from 'sphere-knn';

import NakamalSearchDialog from '@/components/NakamalSearchDialog.vue';
import NewNakamalDialog from '@/components/NewNakamalDialog.vue';
import NetworkStatusDialog from '@/components/NetworkStatusDialog.vue';
import NakamalBottomSheet from '@/components/NakamalBottomSheet.vue';
import NakamalMapPopup from '@/components/NakamalMapPopup.vue';
import NakamalFilterSidebar from '@/components/NakamalFilterSidebar.vue';
import NakamalListItem from '@/components/NakamalListItem.vue';

import Vue2LeafletHeatmap from '@/components/Vue2LeafletHeatmap.vue';

const { L } = window;
const iconMarkerPath = require('../assets/map-marker.svg');
const iconMarkerCheckmarkPath = require('../assets/map-marker-checkmark.svg');
const iconMarkerGeolocationPath = require('../assets/map-marker-geolocation.svg');

export default {
  name: 'NakamalMap',
  mixins: [OfflineMixin],
  components: {
    NakamalBottomSheet,
    NetworkStatusDialog,
    NakamalSearchDialog,
    NewNakamalDialog,
    NakamalMapPopup,
    NakamalFilterSidebar,
    NakamalListItem,
    LMap,
    LTileLayer,
    LMarker,
    LControl,
    LLayerGroup,
    Vue2LeafletHeatmap,
  },
  data() {
    return {
      showHeatmap: false,
      showNearbyNakamals: false,
      nearbyNakamals: [],
      fab: false,
      minZoom: 12,
      maxBounds: latLngBounds([
        [-17.627, 168.11],
        [-17.830, 168.47],
      ]),
      mapOptions: {
        zoomSnap: 0.5,
      },
      icon: icon({
        iconUrl: iconMarkerPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
      iconCheckmark: icon({
        iconUrl: iconMarkerCheckmarkPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
      iconGeolocation: icon({
        iconUrl: iconMarkerGeolocationPath,
        iconSize: [43, 43],
        iconAnchor: [22, 42],
      }),
      // Loading bar variables
      mapLoading: false,
      mapTileLoading: 0,
      mapTileLoaded: 0,
      // Bottom sheet
      bottomSheet: false,
      bottomSheetFull: false,
    };
  },
  computed: {
    ...mapGetters({
      // showDistance: 'map/showDistance', // testing idea - needs refined
      // showDistanceLine: 'map/showDistanceLine',
      // distance: 'map/displayDistance',
      isUserVerified: 'auth/isUserVerified',
      location: 'map/location',
      showLocationProgress: 'map/showLocationProgress',
      bounds: 'map/bounds',
      center: 'map/center',
      zoom: 'map/zoom',
      showNewNakamalMarker: 'map/showNewNakamalMarker',
      nakamals: 'nakamal/filteredList',
      hasFilters: 'nakamal/hasFilters',
      total: 'nakamal/total',
      selectedNakamal: 'nakamal/selected',
      getNakamalHasImages: 'image/nakamalHasImages',
      checkins: 'checkin/list',
      recentCheckins: 'checkin/recent',
      recentNakamalIds: 'checkin/recentNakamalIds',
      darkMode: 'setting/darkMode',
    }),
    checkinHeatmap() {
      // XXX Not as efficient as it could be
      const counts = {};
      let maxCheckins = 1;
      const nakIds = this.nakamals.map((n) => n.id);
      const checkins = this.checkins.filter((c) => nakIds.includes(c.nakamal.id));
      checkins.forEach((c) => {
        const nId = c.nakamal.id;
        counts[nId] = counts[nId] ? counts[nId] + 1 : 1;
        if (counts[nId] > maxCheckins) {
          maxCheckins = counts[nId];
        }
      });
      return checkins.map((c) => {
        let intensity = 0;
        intensity = (counts[c.nakamal.id] / maxCheckins);
        return [c.nakamal.lat, c.nakamal.lng, intensity];
      });
    },
    url() {
      if (this.darkMode) {
        return 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png';
      }
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    },
    attribution() {
      if (this.darkMode) {
        return 'Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.';
      }
      return '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
    },
    tilesLoadingPercent() {
      if (!this.mapLoading) return 100;
      return Math.round((this.mapTileLoaded / this.mapTileLoading) * 100);
    },
  },
  watch: {
    selectedNakamal(n) {
      if (!this.getNakamalHasImages(n.id)) {
        this.$store.dispatch('image/getNakamal', n.id);
      }
    },
  },
  methods: {
    async toggleCheckinHeatmap() {
      if (this.showHeatmap) {
        this.showHeatmap = false;
      } else {
        this.showHeatmap = true;
        await this.$store.dispatch('checkin/getAll');
      }
    },
    getLocationSuccess(pos, result) {
      this.setShowLocationProgress(false);
      if (result === 'success') {
        this.setLocation(pos.coords);
        this.flyTo([pos.coords.latitude, pos.coords.longitude], 18);
        // Testing sphere Knn
        this.findNearestNakamals();
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
      this.setShowLocationProgress(true);
      console.log('Location progress:', pos);
    },
    getLocation() {
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

      // Mock get location
      // this.getLocationSuccess({
      //   coords: {
      //     latitude: this.center.lat,
      //     longitude: this.center.lng,
      //   },
      // }, 'success');
      // return;
      navigator.geolocation.getAccurateCurrentPosition(
        this.getLocationSuccess,
        this.getLocationError,
        this.getLocationProgress,
        {
          desiredAccuracy: 20,
          // minCount: 1,
          desiredAccuracyCountMin: 2,
          maxWait: 15000,
          // enableLowAccuracyOnTimeout: true,
        },
      );
    },
    findNearestNakamals() {
      const lookup = sphereKnn(this.nakamals);
      this.nearbyNakamals = lookup(this.location.latitude, this.location.longitude, 10, 1000);
    },
    flyToNearby(id) {
      this.showNearbyNakamals = false;
      this.markerClick(id);
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
        'setBounds',
        'setCenter',
        'setZoom',
        'setShowNewNakamalMarker',
        'setShowFilters',
        'setShowDetails',
        'setShowSearch',
      ],
    ),
    iconMarker(nakamalId) {
      return this.recentNakamalIds.includes(nakamalId) ? this.iconCheckmark : this.icon;
    },
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
    flyTo(latlng, zoom = 18) {
      this.$refs.map.mapObject.setView(latlng, zoom);
    },
    flyToSelected() {
      this.$refs.nakamalPopup.mapObject.openPopup(this.selectedNakamal.latLng);
      // Adjust targetLatLng to slightly below center to allow space for popup in view
      let targetLatLng = this.selectedNakamal.latLng;
      const targetPoint = this.$refs.map.mapObject.project(targetLatLng, 18).subtract([0, 150]);
      targetLatLng = this.$refs.map.mapObject.unproject(targetPoint, 18);
      this.flyTo(targetLatLng);
    },
    flyToBounds() {
      this.$nextTick().then(() => {
        if (this.nakamals.length === 0) {
          this.$refs.map.mapObject.flyToBounds(this.maxBounds, { duration: 1.0 });
        } else {
          const bounds = latLngBounds(this.nakamals.map((n) => n.latLng));
          this.$refs.map.mapObject.flyToBounds(bounds, { duration: 1.0, padding: [50, 50] });
        }
      });
    },
    markerClick(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.flyToSelected();
        });
      // .then(() => {
      //   this.setShowDetails(true);
      // });
    },
    tileLoadComplete() {
      setTimeout(() => {
        this.mapLoading = false;
        this.mapTileLoading = 0;
        this.mapTileLoaded = 0;
      }, 500);
    },
  },
  async created() {
    this.$store.dispatch('map/RESET');
    this.$root.$on('fly-to-selected', this.flyToSelected);
    this.$root.$on('fly-to-bounds', this.flyToBounds);
  },
  async mounted() {
    // this.loading = true;
    await this.$store.dispatch('nakamal/load');
    await this.$store.dispatch('checkin/getRecent');
    // this.loading = false;
    if (this.selectedNakamal) {
      setTimeout(() => {
        this.flyToSelected();
      }, 500);
    }
  },
};
</script>

<style scoped>
.map-online {
  height: calc(100vh - 50px);
}
.map-offline {
  height: calc(100vh - 80px);
}
.example-custom-control > .v-card {
  z-index: 2000;
}
#map-wrapper > .v-progress {
  z-index: 2000;
}
</style>
