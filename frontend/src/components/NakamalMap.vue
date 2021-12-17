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

      <l-layer-group ref="nakamalPopup">
        <l-popup
          :options="{ offset: popupOffset }"
          @popupclose="popupClosed"
        >
          <h3 class="mb-2 font-weight-bold">{{ selectedNakamal.name }}</h3>
          <v-img
            v-if="selectedNakamalImage"
            contain
            height="100"
            :src="selectedNakamalImage.thumbnail"
          ></v-img>
          <ul class="mb-2 font-weight-light">
            <li>Light: {{ selectedNakamal.light || '-' }}</li>
            <li>Windows: {{ selectedNakamal.windows || '-' }}</li>
            <li>Other Names: {{ aliasNames(selectedNakamal.aliases) }}</li>
          </ul>
          <v-btn
            small
            block
            outlined
            color="primary"
            :to="{ name: 'Nakamal', params: { id: selectedNakamal.id } }"
          >
            View Page
          </v-btn>
        </l-popup>
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
                color="primary darken-2"
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
              color="primary lighten-1"
              @click.stop="getLocation"
            >
              <v-icon>mdi-crosshairs-gps</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="primary lighten-2"
              @click.stop="setShowSearch(true)"
            >
              <v-icon>mdi-magnify</v-icon>
            </v-btn>
            <v-btn
              fab
              dark
              small
              color="primary lighten-3"
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
  </v-container>
</template>

<script>
import {
  mapActions,
  mapGetters,
} from 'vuex';
import {
  icon, latLngBounds, point,
} from 'leaflet';
import {
  LMap, LTileLayer, LMarker, LPopup, LControl, LLayerGroup,
} from 'vue2-leaflet';
import NakamalSearchDialog from '@/components/NakamalSearchDialog.vue';
import NewNakamalDialog from '@/components/NewNakamalDialog.vue';
import NetworkStatusDialog from '@/components/NetworkStatusDialog.vue';
import NakamalBottomSheet from '@/components/NakamalBottomSheet.vue';

const iconMarkerPath = require('../assets/map-marker.svg');
const iconMarkerCheckmarkPath = require('../assets/map-marker-checkmark.svg');

export default {
  name: 'NakamalMap',
  components: {
    NakamalBottomSheet,
    NetworkStatusDialog,
    NakamalSearchDialog,
    NewNakamalDialog,
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
    LControl,
    LLayerGroup,
  },
  data() {
    return {
      fab: false,
      // zoom: 18,
      // center: latLng(-17.741526, 168.312024),
      // bounds: latLngBounds([
      //   [-17.667, 168.21],
      //   [-17.830, 168.47],
      // ]),
      minZoom: 12,
      maxBounds: latLngBounds([
        [-17.627, 168.11],
        [-17.830, 168.47],
      ]),
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      // withPopup: latLng(-17.751526, 168.2421994),
      // withTooltip: latLng(-17.748758, 168.308369),
      // currentZoom: 18,
      // currentCenter: latLng(-17.741526, 168.312024),
      mapOptions: {
        zoomSnap: 0.5,
      },
      popupOffset: point(0, -30),
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
      nakamals: 'nakamal/list',
      total: 'nakamal/total',
      selectedNakamal: 'nakamal/selected',
      getNakamalImages: 'image/nakamal',
      getNakamalHasImages: 'image/nakamalHasImages',
      recentCheckins: 'checkin/recent',
      recentNakamalIds: 'checkin/recentNakamalIds',
    }),
    selectedNakamalImage() {
      if (this.selectedNakamal) {
        if (this.getNakamalHasImages(this.selectedNakamal.id)) {
          return this.getNakamalImages(this.selectedNakamal.id)[0];
        }
      }
      return null;
    },
    tilesLoadingPercent() {
      if (!this.mapLoading) return 100;
      return Math.round((this.mapTileLoaded / this.mapTileLoading) * 100);
    },
    // activeFab() {
    //   switch (this.mode)
    // }
  },
  watch: {
    selectedNakamal(n) {
      if (!this.getNakamalHasImages(n.id)) {
        this.$store.dispatch('image/getNakamal', n.id);
      }
    },
  },
  methods: {
    aliasNames(aliases) {
      if (!aliases) return '-';
      return aliases.join(', ');
    },
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
      'map', [
        'setLocation',
        'setBounds',
        'setCenter',
        'setZoom',
        'setShowNewNakamalMarker',
        'setShowDetails',
        'setShowSearch',
      ],
    ),
    iconMarker(nakamalId) {
      return this.recentNakamalIds.includes(nakamalId) ? this.iconCheckmark : this.icon;
    },
    newNakamalMarker() {
      this.fab = false;
      this.setShowNewNakamalMarker(true);
    },
    flyTo(latlng, zoom = 18) {
      this.$refs.map.mapObject.setView(latlng, zoom);
    },
    flyToSelected() {
      this.$refs.nakamalPopup.mapObject.openPopup(this.selectedNakamal.latLng);
      this.flyTo(this.selectedNakamal.latLng);
    },
    markerClick(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.flyToSelected();
        });
    },
    popupClosed() {
      this.$store.dispatch('nakamal/unselect');
    },
    tileLoadComplete() {
      setTimeout(() => {
        this.mapLoading = false;
        this.mapTileLoading = 0;
        this.mapTileLoaded = 0;
      }, 500);
    },
  },
  beforeMount() {
    this.$store.dispatch('nakamal/load');
    this.$store.dispatch('checkin/getRecent');
    this.$root.$on('fly-to-selected', this.flyToSelected);
  },
  mounted() {
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
