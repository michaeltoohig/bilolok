<template>
  <BaseTimelineCard
    :timestamp="item.start_at"
    :user="user"
    :nakamal="nakamal"
    :linkNakamal="linkNakamal"
  >
    <template v-slot:card-action>
      <BaseTimelineCardMenu
        :on-share="onShare"
        :on-delete="onDelete"
        :user-can-delete="userCanDelete"
      ></BaseTimelineCardMenu>
    </template>
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
          v-if="nakamal"
          :icon="icon"
          :lat-lng="nakamal.latLng"
        >
          <l-tooltip :options="{
            permanent: 'true',
            direction: 'bottom',
          }">
            {{ nakamal.name }}
          </l-tooltip>
        </l-marker>
      </l-map>
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import { domain } from '@/env';
import {
  latLngBounds, icon,
} from 'leaflet';
import {
  LMap, LTileLayer, LPolyline, LMarker, LTooltip,
} from 'vue2-leaflet';
import { mapActions, mapGetters } from 'vuex';
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';
import BaseTimelineCardMenu from '@/components/timeline/BaseTimelineCardMenu.vue';

const iconMarkerPath = require('@/assets/map-marker.svg');

export default {
  name: 'TripTimelineCard',
  components: {
    BaseTimelineCard,
    BaseTimelineCardMenu,
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
      user: null,
      nakamal: null,
      icon: icon({
        iconUrl: iconMarkerPath,
        iconSize: [54, 44],
        iconAnchor: [16, 40],
      }),
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      currentUser: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
      darkMode: 'setting/darkMode',
    }),
    isMine() {
      if (!this.user || !this.isLoggedIn) return false;
      return this.user.id === this.currentUser.id;
    },
    userCanDelete() {
      return this.isMine || this.hasAdminAccess;
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
    bounds() {
      return latLngBounds(this.item.data);
    },
  },
  methods: {
    async onShare() {
      const text = `User's trip to ${this.nakamal.name} on Bilolok!`;
      const url = `${domain}/trip/${this.item.id}`;
      if (navigator.share) {
        const { title } = document;
        navigator.share({
          url,
          title,
          text,
        }).then(() => {
          this.$store.dispatch('notify/add', {
            title: 'Thanks For Sharing!',
            text: 'We appreciate you letting others know about Bilolok.',
            type: 'primary',
          });
        });
      } else {
        if (!navigator.clipboard) {
          await this.$store.dispatch('notify/add', {
            title: 'Share Not Available',
            text: 'Your device does not support sharing.',
            type: 'error',
          });
          return;
        }
        await navigator.clipboard.writeText(`${text} ${url}`);
        await this.$store.dispatch('notify/add', {
          title: 'Copied to Clipboard!',
          text: 'We appreciate you letting others know about Bilolok.',
          type: 'primary',
        });
      }
    },
    onDelete() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm(this.$i18n.t('trip.confirm_delete'))) {
        this.$store.dispatch('trip/remove', this.item.id);
      }
    },
    ...mapActions({
      loadUser: 'user/loadOne',
      loadNakamal: 'nakamal/loadOne',
    }),
  },
  async created() {
    if (this.item.nakamal) {
      this.nakamal = await this.loadNakamal(this.item.nakamal);
    }
    this.user = await this.loadUser(this.item.user);
  },
};
</script>

<style scoped>
#map-wrapper {
  height: 400px;
}
</style>
