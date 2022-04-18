<template>
  <v-card class="elevation-2 mb-3">
    <v-card-title class="d-flex flex-row justify-space-between">
      <h2 :class="`headline font-weight-light ${this.color}--text`">
        Trip
      </h2>
    </v-card-title>
    <v-card-subtitle>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <span
            v-bind="attrs"
            v-on="on"
          >
            <strong>{{ formatTimeAgo(item.start_at) }}</strong>
          </span>
        </template>
        <span>{{ formatTime(item.start_at) }}</span>
      </v-tooltip>
    </v-card-subtitle>
    <v-card-text id="map-wrapper">
      <l-map
        style="z-index: 0;"
        ref="map"
        :bounds="bounds"
        :options="{
          keyboard: false,
          dragging: false,
          zoomControl: false,
          boxZoom: false,
          doubleClickZoom: false,
          scrollWheelZoom: false,
          tap: false,
          touchZoom: false,
        }"
      >
        <l-tile-layer
          :url="url"
          :attribution="attribution"
        />
        <l-polyline
          :lat-lngs="item.data"
          :weight="5"
        ></l-polyline>
        <l-marker
          :icon="icon"
          :lat-lng="item.nakamal.latLng"
        >
          <l-tooltip :options="{
            permanent: 'true',
            direction: 'bottom',
          }">
            {{ item.nakamal.name }}
          </l-tooltip>
        </l-marker>
      </l-map>
    </v-card-text>
    <v-list-item v-if="linkNakamal">
      <v-list-item-avatar
        v-if="nakamalAvatar(item.nakamal.id)"
        color="grey darken-3"
        class="nakamal-avatar"
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'Nakamal', params: { id: item.nakamal.id } })"
      >
        <v-img :src="nakamalAvatar(item.nakamal.id).thumbnail"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          {{ item.nakamal.name }}
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn
          outlined
          small
          icon
          link
          :to="{ name: 'Nakamal', params: { id: item.nakamal.id } }"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
    <v-list-item v-if="linkUser">
      <v-list-item-avatar
        color="grey darken-3 elevation-2 user-avatar"
        tile
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'User', params: { id: item.user.id } })"
      >
        <v-img :src="item.user.avatar"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn
          outlined
          small
          icon
          link
          :to="{ name: 'User', params: { id: item.user.id } }"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
  </v-card>
</template>

<script>
import {
  latLngBounds, icon,
} from 'leaflet';
import {
  LMap, LTileLayer, LPolyline, LMarker, LTooltip,
} from 'vue2-leaflet';
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

const iconMarkerPath = require('@/assets/map-marker.svg');

export default {
  name: 'CardTrip',
  props: {
    item: {
      type: Object,
      required: true,
    },
    linkUser: {
      type: Boolean,
      default: false,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  mixins: [formatDatetime],
  components: {
    LMap,
    LTileLayer,
    LPolyline,
    LMarker,
    LTooltip,
  },
  data() {
    return {
      color: 'green',
      icon: icon({
        iconUrl: iconMarkerPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
    };
  },
  computed: {
    ...mapGetters({
      getNakamalImages: 'image/nakamal',
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
    bounds() {
      return latLngBounds(this.item.data);
    },
  },
  methods: {
    nakamalAvatar(nakamalId) {
      const images = this.getNakamalImages(nakamalId);
      if (images.length > 0) {
        return images[0];
      }
      return null;
    },
  },
};
</script>

<style scoped>
.nakamal-avatar,
.user-avatar {
  cursor: pointer;
}

#map-wrapper {
  height: 400px;
}
</style>
