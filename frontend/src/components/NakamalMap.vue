/* eslint-disable */

<template>
  <v-container
    fluid
    id="map-wrapper"
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

      <l-marker
        v-if="location"
        :icon="icon"
        :lat-lng="[location.latitude, location.longitude]"
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
            <v-btn
              fab
              dark
              small
              color="secondary darken-1"
              @click.stop="getLocation"
            >
              <v-icon>mdi-crosshairs-gps</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="secondary darken-1"
              @click.stop="setShowSearch(true)"
            >
              <v-icon>mdi-map-search</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="secondary darken-1"
              @click.stop="setShowFilters(true)"
            >
              <v-icon>mdi-map-marker-minus</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="secondary darken-1"
              @click.stop="newNakamalMarker"
            >
              <v-icon>mdi-map-marker-plus</v-icon>
            </v-btn>
          </v-speed-dial>
        </v-fab-transition>
      </l-control>
    </l-map>

    <NakamalSearchDialog></NakamalSearchDialog>

    <NakamalBottomSheet></NakamalBottomSheet>

    <NakamalFilterSidebar></NakamalFilterSidebar>
  </v-container>
</template>

<script>
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
import NakamalSearchDialog from '@/components/NakamalSearchDialog.vue';
import NewNakamalDialog from '@/components/NewNakamalDialog.vue';
import NetworkStatusDialog from '@/components/NetworkStatusDialog.vue';
import NakamalBottomSheet from '@/components/NakamalBottomSheet.vue';
import NakamalMapPopup from '@/components/NakamalMapPopup.vue';
import NakamalFilterSidebar from '@/components/NakamalFilterSidebar.vue';

const iconMarkerPath = require('../assets/map-marker.svg');
const iconMarkerCheckmarkPath = require('../assets/map-marker-checkmark.svg');

export default {
  name: 'NakamalMap',
  components: {
    NakamalBottomSheet,
    NetworkStatusDialog,
    NakamalSearchDialog,
    NewNakamalDialog,
    NakamalMapPopup,
    NakamalFilterSidebar,
    LMap,
    LTileLayer,
    LMarker,
    LControl,
    LLayerGroup,
  },
  data() {
    return {
      drawer: true,
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
      isUserVerified: 'auth/isUserVerified',
      location: 'map/location',
      bounds: 'map/bounds',
      center: 'map/center',
      zoom: 'map/zoom',
      showNewNakamalMarker: 'map/showNewNakamalMarker',
      nakamals: 'nakamal/filteredList',
      hasFilters: 'nakamal/hasFilters',
      total: 'nakamal/total',
      selectedNakamal: 'nakamal/selected',
      getNakamalHasImages: 'image/nakamalHasImages',
      recentCheckins: 'checkin/recent',
      recentNakamalIds: 'checkin/recentNakamalIds',
      darkMode: 'setting/darkMode',
    }),
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
    getLocation() {
      if (!('geolocation' in navigator)) {
        console.log('Geolocation is not available.');
        return;
      }
      // get position
      navigator.geolocation.getCurrentPosition((pos) => {
        console.log(pos);
        this.setLocation(pos.coords);
        this.flyTo([pos.coords.latitude, pos.coords.longitude], 18);
      }, (error) => {
        console.log('error getting location', error);
      });
    },
    ...mapActions(
      'nakamal', [
        'removeFilters',
      ],
    ),
    ...mapActions(
      'map', [
        'setLocation',
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
#map-wrapper {
  height: calc(100vh - 50px);
}
.example-custom-control > .v-card {
  z-index: 2000;
}
#map-wrapper > .v-progress {
  z-index: 2000;
}
</style>
