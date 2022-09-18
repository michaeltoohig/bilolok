<template>
  <l-popup
    :options="{ offset: popupOffset }"
    @popupclose="popupClosed"
  >
    <h3 class="mb-2 text-h6 font-weight-bold">{{ selectedNakamal.name }}</h3>
    <div class="d-flex justify-center">
      <v-badge
        v-if="profile"
        :color="selectedNakamal.lightBadge.color"
        :icon="selectedNakamal.lightBadge.icon"
        overlap
        bordered
        left
        dark
      >
        <v-avatar
          @click="goToNakamal"
          class="nakamal-avatar"
          tile
          size="114"
        >
          <v-img
            height="114"
            contain
            :src="profile.thumbnail"
          ></v-img>
        </v-avatar>
      </v-badge>
    </div>
    <v-list light dense>
      <v-list-item v-if="selectedNakamal.aliases.length">
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">
            {{ $t('nakamal.attrs.other_names') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ aliasNames(selectedNakamal.aliases) }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="location">
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">
            {{ $t('map.compass.distance') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ displayDistance }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item v-if="!profile">
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">
            {{ $t('nakamal.attrs.light') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ selectedNakamal.light }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">
            {{ $t('nakamal.attrs.number_of_windows') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ selectedNakamal.windows || '-' }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">
            {{ $t('nakamal.attrs.area') }}
          </v-list-item-title>
          <v-list-item-subtitle>
            <span v-if="selectedNakamal.area">
              {{ selectedNakamal.area.name }}
            </span>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-btn
      small
      block
      outlined
      color="primary"
      :to="{ name: 'Nakamal', params: { id: selectedNakamal.id } }"
    >
      {{ $t('nakamal.view_page') }}
    </v-btn>
    <v-btn
      small
      block
      color="primary"
      class="mt-3"
      @click="clickCompass"
    >
      <v-icon small class="mr-1">mdi-compass</v-icon>
      {{ $t('map.compass.compass') }}
    </v-btn>
  </l-popup>
</template>

<script>
import {
  mapActions,
  mapGetters,
} from 'vuex';
import {
  latLng,
  point,
} from 'leaflet';
import {
  LPopup,
} from 'vue2-leaflet';

export default {
  name: 'NakamalMapPopup',
  components: {
    LPopup,
  },
  data() {
    return {
      popupOffset: point(0, -30),
    };
  },
  computed: {
    ...mapGetters({
      center: 'map/center',
      location: 'map/location',
      selectedNakamal: 'nakamal/selected',
      // getNakamalImages: 'image/nakamal',
      // getNakamalHasImages: 'image/nakamalHasImages',
    }),
    displayDistance() {
      if (!this.location) return null;
      const locLatLng = latLng(this.location.latitude, this.location.longitude);
      let distance = Math.round(locLatLng.distanceTo(this.selectedNakamal.latLng));
      if (distance < 1000) {
        distance = `${distance} meters`;
      } else {
        distance = (distance / 1000).toFixed(1);
        distance = `${distance} kilometers`;
      }
      return distance;
    },
    profile() {
      if (this.selectedNakamal && this.selectedNakamal.profile) {
        return this.$store.getters['image/find'](this.selectedNakamal.profile);
      } else {
        return null;
      }
    },
  },
  methods: {
    ...mapActions({
      loadProfile: 'image/loadOne',
    }),
    goToNakamal() {
      this.$router.push({ name: 'Nakamal', params: { id: this.selectedNakamal.id } });
    },
    clickCompass() {
      this.$emit('compass');
    },
    popupClosed() {
      this.$store.dispatch('nakamal/unselect');
    },
    aliasNames(aliases) {
      if (!aliases) return '-';
      return aliases.join(', ');
    },
  },
  async mounted() {
    if (this.selectedNakamal.profile) {
      await this.loadProfile(this.selectedNakamal.profile);
    }
  },
};
</script>

<style scoped>
.v-list-item {
  padding: 0;
}
</style>
