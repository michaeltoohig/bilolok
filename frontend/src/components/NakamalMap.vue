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

      <NewNakamalDialog></NewNakamalDialog>

      <l-marker
        v-if="location"
        :icon="iconGeolocation"
        :lat-lng="[location.latitude, location.longitude]"
        @click="clickUserLocation"
      ></l-marker>

      <div v-if="showMarkers">
        <l-marker
          v-for="nakamal in nakamals"
          :key="nakamal.id"
          :icon="iconMarker(nakamal.id)"
          :lat-lng="nakamal.latLng"
          @click="markerClick(nakamal.id)"
        >
          <l-tooltip :options="{
            direction: 'bottom',
          }">
            {{ nakamal.name }}
          </l-tooltip>
        </l-marker>
      </div>
      <div v-else>
        <l-circle
          v-for="area in mapAreas"
          :key="area.name"
          :lat-lng="area.latLng"
          :radius="area.radius"
          :color="color"
        >
          <l-tooltip
            class="area-tooltip text-center"
            :options="{
              permanent: true,
              interactive: true,
              direction: 'center',
              opacity: 0.85,
            }"
          >
            <h2 @click="areaClick(area.name)">{{ area.name }}</h2>
            <p class="mb-0">
              <strong>{{ area.nakamals }}</strong> Kava Bars
            </p>
          </l-tooltip>
        </l-circle>
      </div>

      <l-layer-group v-if="selectedNakamal" ref="nakamalPopup">
        <NakamalMapPopup v-on:compass="startCompassModeWithIntro"></NakamalMapPopup>
      </l-layer-group>

      <l-control
        :position="'bottomleft'"
      >
        <NetworkStatusDialog></NetworkStatusDialog>
      </l-control>

      <l-control
        :position="'bottomright'"
      >
        <NakamalMapFabButtons></NakamalMapFabButtons>
      </l-control>

      <l-control
        :position="'topright'"
      >
        <Compass v-on:stop="setStopCompassMode"></Compass>
      </l-control>

      <LPolyline :lat-lngs="compassModePolylineLocations"></LPolyline>

      <LPolyline
        v-for="trip in recentTrips"
        :key="trip.id"
        :lat-lngs="trip.data"
        :color="color"
        :weight="5"
      >
        <LTooltip
          :options="{
            sticky: true,
            direction: 'bottom',
          }"
        >
          <v-avatar>
            <v-img :src="trip.user.avatar"></v-img>
          </v-avatar>
        </LTooltip>
        <LPopup>
          <div class="d-flex flex-column align-center justify-center text-center">
            <v-avatar
              class="mb-2"
              v-ripple="{ center: true }"
              @click="goToUser(trip.user.id)"
            >
              <v-img :src="trip.user.avatar"></v-img>
            </v-avatar>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span
                  v-bind="attrs"
                  v-on="on"
                >
                  <strong>{{ formatTimeAgo(trip.start_at) }}</strong>
                </span>
              </template>
              <span>{{ formatTime(trip.start_at) }}</span>
            </v-tooltip>
            <span class="font-weight-normal">Headed to:</span>
            <h3 class="text-h6 font-weight-bold mb-2">{{ trip.nakamal.name }}</h3>
            <v-btn
              outlined
              small
              color="primary"
              @click="markerClick(trip.nakamal.id)"
            >
              View Kava Bar
            </v-btn>
          </div>
        </LPopup>
      </LPolyline>

      <Vue2LeafletHeatmap
        v-if="heatmapCheckins && showHeatmapLayer"
        :visible="showHeatmapLayer"
        :lat-lng="heatmapCheckins"
        :radius="20"
        :min-opacity=".50"
        :max-zoom="16"
        :blur="18"
      ></Vue2LeafletHeatmap>
    </l-map>

    <NakamalSearchDialog></NakamalSearchDialog>

    <NakamalBottomSheet></NakamalBottomSheet>

    <NakamalFilterSidebar></NakamalFilterSidebar>

    <NakamalHeatmapSidebar></NakamalHeatmapSidebar>

    <LocationProgressDialog></LocationProgressDialog>

    <CompassModeIntroDialog
      :show="showCompassModeIntroDialog"
      v-on:hide="() => { showCompassModeIntroDialog = false; }"
    ></CompassModeIntroDialog>

    <v-dialog
      v-model="showNearbyNakamals"
      persistent
      scrollable
      width="500"
      color="primary"
    >
      <v-card>
        <v-card-title >
          Nearby Kava Bars
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="py-3" v-if="nearbyNakamals.length > 0">
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

    <v-dialog
      persistent
      v-model="loading"
      max-width="360"
    >
      <v-card
        min-height="250"
      >
        <v-container fill-height>
          <v-layout align-center justify-center>
            <v-flex>
              <div class="text-center">
                <div class="headline my-5">Loading Kava Bars...</div>
                <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
              </div>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import OfflineMixin from '@/mixins/offline';
import FormatDatetime from '@/mixins/formatDatetime';
import {
  mapActions,
  mapGetters,
} from 'vuex';
import {
  icon, latLng, latLngBounds, Symbol,
} from 'leaflet';
import {
  LMap, LTileLayer, LMarker, LTooltip, LControl, LLayerGroup, LPolyline, LCircle, LPopup,
} from 'vue2-leaflet';
// import { AntPath } from 'leaflet-ant-path';
import sphereKnn from 'sphere-knn';

import NakamalMapFabButtons from '@/components/NakamalMapFabButtons.vue';
import NakamalSearchDialog from '@/components/NakamalSearchDialog.vue';
import NewNakamalDialog from '@/components/NewNakamalDialog.vue';
import NetworkStatusDialog from '@/components/NetworkStatusDialog.vue';
import NakamalBottomSheet from '@/components/NakamalBottomSheet.vue';
import NakamalMapPopup from '@/components/NakamalMapPopup.vue';
import NakamalFilterSidebar from '@/components/NakamalFilterSidebar.vue';
import NakamalHeatmapSidebar from '@/components/NakamalHeatmapSidebar.vue';
import NakamalListItem from '@/components/NakamalListItem.vue';
import Compass from '@/components/Compass.vue';
import CompassModeIntroDialog from '@/components/CompassModeIntroDialog.vue';
import LocationProgressDialog from '@/components/LocationProgressDialog.vue';

import Vue2LeafletHeatmap from '@/components/Vue2LeafletHeatmap.vue';

// const { L } = window;
const iconMarkerPath = require('../assets/map-marker.svg');
const iconMarkerCheckmarkPath = require('../assets/map-marker-checkmark.svg');
const iconMarkerGeolocationPath = require('../assets/map-marker-geolocation.svg');

export default {
  name: 'NakamalMap',
  mixins: [FormatDatetime, OfflineMixin],
  components: {
    NakamalMapFabButtons,
    NakamalBottomSheet,
    NetworkStatusDialog,
    NakamalSearchDialog,
    NewNakamalDialog,
    NakamalMapPopup,
    NakamalFilterSidebar,
    NakamalHeatmapSidebar,
    NakamalListItem,
    Compass,
    CompassModeIntroDialog,
    LocationProgressDialog,
    LMap,
    LTileLayer,
    LMarker,
    LTooltip,
    LControl,
    LLayerGroup,
    LPolyline,
    LCircle,
    LPopup,
    Vue2LeafletHeatmap,
  },
  data() {
    return {
      loading: true,
      showCompassModeIntroDialog: false,
      showNearbyNakamals: false,
      nearbyNakamals: [],
      minZoom: 12,
      maxBoundsPortVila: latLngBounds([
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

      showMarkers: true,
    };
  },
  computed: {
    ...mapGetters({
      // showDistance: 'map/showDistance', // testing idea - needs refined
      // showDistanceLine: 'map/showDistanceLine',
      // distance: 'map/displayDistance',
      showHeatmap: 'map/showHeatmap',
      location: 'map/location',
      compassMode: 'map/compassMode',
      skipCompassModeIntro: 'map/skipCompassModeIntro',
      compassModePolyline: 'map/compassModePolyline',
      bounds: 'map/bounds',
      center: 'map/center',
      zoom: 'map/zoom',
      showHeatmapLayer: 'map/showHeatmap',
      hasFilters: 'nakamal/hasFilters',
      nakamals: 'nakamal/filteredList',
      total: 'nakamal/total',
      selectedNakamal: 'nakamal/selected',
      getNakamalHasImages: 'image/nakamalHasImages',
      checkins: 'checkin/filteredList',
      recentCheckins: 'checkin/recent',
      recentNakamalIds: 'checkin/recentNakamalIds',
      recentTrips: 'trip/recent',
      darkMode: 'setting/darkMode',
    }),
    maxBounds() {
      if (this.compassMode && this.location) {
        const targetLatLng = latLng(this.location.latitude, this.location.longitude);
        return latLngBounds([targetLatLng, targetLatLng]);
      }
      return this.maxBoundsPortVila;
    },
    mapAreas() {
      const areas = [];
      const filteredNakamals = this.nakamals.filter((n) => n.area.name !== 'UNDEFINED');
      const naks = filteredNakamals.reduce((groups, n) => ({
        ...groups,
        [n.area.name]: [...(groups[n.area.name] || []), n],
      }), {});
      Object.keys(naks).forEach((area) => {
        const center = latLngBounds(naks[area].map((n) => n.latLng)).getCenter();
        const radius = naks[area].reduce((maxDist, n) => {
          const dist = center.distanceTo(n.latLng);
          return dist > maxDist ? dist : maxDist;
        }, 250);
        areas.push({
          name: area,
          latLng: center,
          radius,
          nakamals: naks[area].length,
        });
      });
      return areas;
    },
    compassModePolylineLocations() {
      return this.compassModePolyline.map((i) => [i.lat, i.lng]);
    },
    heatmapCheckins() {
      // XXX Not as efficient as it could be
      let checkins = null;
      const counts = {};
      let maxCheckins = 1;
      if (this.hasFilters) {
        const nakIds = this.nakamals.map((n) => n.id);
        checkins = this.checkins.filter((c) => nakIds.includes(c.nakamal.id));
      } else {
        checkins = this.checkins;
      }
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
    color() {
      if (this.darkMode) {
        return 'grey';
      }
      return 'blue';
    },
    patterns() {
      return [
        {
          offset: 25,
          repeat: 100,
          symbol: Symbol.arrowHead({
            pixelSize: 14,
            pathOptions: {
              fillOpacity: 1,
              weight: 0,
              color: this.color,
            },
          }),
        },
      ];
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
    zoom(val) {
      if (val > 16) {
        this.showMarkers = true;
      }
      if (val <= 13) {
        this.showMarkers = false;
      }
      return val;
    },
  },
  methods: {
    goToUser(id) {
      this.$router.push({ name: 'User', params: { id } });
    },
    startCompassModeWithIntro() {
      if (this.skipCompassModeIntro) {
        this.startCompassMode();
        return;
      }
      this.showCompassModeIntroDialog = true;
    },
    async setStopCompassMode() {
      await this.stopCompassMode();
      this.flyToSelected();
    },
    clickUserLocation() {
      this.findNearestNakamals();
      this.showNearbyNakamals = true;
    },
    getTripLatLngs(data) {
      return data.map((i) => latLng(i.lat, i.lng));
    },
    // getLocationSuccess(pos, result) {
    //   this.setShowLocationProgress(false);
    //   if (result === 'success') {
    //     this.setLocation(pos.coords);
    //     this.flyTo([pos.coords.latitude, pos.coords.longitude], 18);
    //     // // Testing sphere Knn
    //     // this.findNearestNakamals();
    //   } else {
    //     this.getLocationError({});
    //   }
    // },
    // getLocationError(error) {
    //   console.log('Location error:', error);
    //   this.setShowLocationProgress(false);
    //   this.$store.dispatch('notify/add', {
    //     title: 'Location Not Found',
    //     text: 'Your device did not provide an accurate location.',
    //     color: 'error',
    //     duration: 5_000,
    //   });
    // },
    // getLocationProgress(pos) {
    //   this.setShowLocationProgress(true);
    // },
    // getLocation() {
    //   if (!('geolocation' in navigator)) {
    //     this.$store.dispatch('notify/add', {
    //       title: 'Location Not Available',
    //       text: 'Your device does not provide location or you have blocked location access.',
    //       color: 'info',
    //       duration: 5_000,
    //     });
    //     return;
    //   }
    //   // get position
    //   this.setShowLocationProgress(true);
    //   navigator.geolocation.getAccurateCurrentPosition(
    //     this.getLocationSuccess,
    //     this.getLocationError,
    //     this.getLocationProgress,
    //     {
    //       desiredAccuracy: 20,
    //       desiredAccuracyCountMin: 2,
    //       maxWait: 15000,
    //     },
    //   );
    // },
    findNearestNakamals() {
      const lookup = sphereKnn(this.nakamals);
      this.nearbyNakamals = lookup(this.location.latitude, this.location.longitude, 10, 1000);
    },
    flyToNearby(id) {
      this.showNearbyNakamals = false;
      this.markerClick(id);
    },
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
      ],
    ),
    iconMarker(nakamalId) {
      return this.recentNakamalIds.includes(nakamalId) ? this.iconCheckmark : this.icon;
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
    areaClick(area) {
      const naks = this.nakamals.filter((n) => n.area.name === area);
      const bounds = latLngBounds(naks.map((n) => n.latLng));
      this.$refs.map.mapObject.flyToBounds(bounds, { duration: 1.0, padding: [50, 50] });
      this.showMarkers = true;
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
    // I want to remove this RESET and return to previous state when returning to this view
    // TODO:
    //  - Heatmap sidebar state does not match heatmap layer on page refresh
    //  - Need to test handling during compass mode
    this.$store.dispatch('map/RESET');
    this.$root.$on('fly-to-selected', this.flyToSelected);
    this.$root.$on('fly-to-bounds', this.flyToBounds);
    this.$root.$on('fly-to', this.flyTo);
  },
  async mounted() {
    this.loading = true;
    await this.$store.dispatch('nakamal/load');
    this.loading = false;
    await this.$store.dispatch('checkin/getRecent');
    await this.$store.dispatch('trip/getRecent');
    if (this.selectedNakamal) {
      setTimeout(() => {
        this.flyToSelected();
      }, 500);
    }
  },
  async beforeDestroy() {
    // Find out if we can keep watching until explicitly cancelled
    // Maybe add a route block to ask if user wants to leave map view while watcher is active
    await this.$store.dispatch('map/clearWatcher');
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

.area-tooltip > p {
  font-size: 9px;
}
</style>
