<template>
  <BaseTimelineCard
    :timestamp="item.start_at"
    :user="item.user"
    :nakamal="item.nakamal"
    :linkNakamal="linkNakamal"
  >
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
  </BaseTimelineCard>
</template>

<script>
import {
  latLngBounds, icon,
} from 'leaflet';
import {
  LMap, LTileLayer, LPolyline, LMarker, LTooltip,
} from 'vue2-leaflet';
import { mapGetters } from 'vuex';
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';

const iconMarkerPath = require('@/assets/map-marker.svg');

export default {
  name: 'TripTimelineCard',
  components: {
    BaseTimelineCard,
    LMap,
    LTileLayer,
    LPolyline,
    LMarker,
    LTooltip,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      icon: icon({
        iconUrl: iconMarkerPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
    };
  },
  computed: {
    ...mapGetters({
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
};
</script>

<style scoped>
#map-wrapper {
  height: 400px;
}
</style>
