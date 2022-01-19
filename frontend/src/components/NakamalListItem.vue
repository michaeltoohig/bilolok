<template>
  <v-card
    class="mx-auto"
    max-width="400"
  >
    <v-img
      v-if="hasImages"
      class="white--text align-end"
      height="200px"
      :src="images[0].thumbnail"
    >
      <v-card-title></v-card-title>
    </v-img>

    <v-card-title class="pb-0">
      {{ nakamal.name }}
    </v-card-title>
    <v-card-subtitle v-if="nakamal.aliases.length > 0" class="pt-2">
      {{ nakamal.aliases.join(', ') }}
    </v-card-subtitle>

    <v-card-text class="text--primary">
      <v-row>
        <v-col cols="6">
          <div class="font-weight-light">
            Distance:
            <span class="font-weight-bold">{{ displayDistance }}</span>
          </div>
          <div class="font-weight-light">
            Light:
            <span class="font-weight-bold">{{ nakamal.light }}</span>
          </div>
          <div class="font-weight-light">
            Windows:
            <span class="font-weight-bold">{{ nakamal.windows || '-' }}</span>
          </div>
        </v-col>
        <v-col cols="6">
          <div class="font-weight-light">
            Area:
            <span class="font-weight-bold">{{ nakamal.area.name }}</span>
          </div>
          <div class="font-weight-light">
            Kava Source:
            <span class="font-weight-bold">{{ kavaSource(nakamal.kava_source) }}</span>
          </div>
          <div class="font-weight-light">
          </div>
        </v-col>
      </v-row>
    </v-card-text>

    <v-card-actions>
      <v-btn
        text
        outlined
        @click="viewPage(nakamal.id)"
      >
        View Page
      </v-btn>
      <v-btn
        text
        outlined
        @click="viewMap(nakamal.id)"
      >
        View on Map
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { latLng } from 'leaflet';
import { mapGetters } from 'vuex';

export default {
  name: 'NakamalListItem',
  props: ['nakamal'],
  computed: {
    ...mapGetters({
      location: 'map/location',
      getImages: 'image/nakamal',
    }),
    hasImages() {
      return this.images.length > 0;
    },
    images() {
      return this.getImages(this.nakamal.id);
    },
    displayDistance() {
      if (!this.location) return null;
      const locLatLng = latLng(this.location.latitude, this.location.longitude);
      let distance = Math.round(locLatLng.distanceTo(this.nakamal.latLng));
      if (distance < 1000) {
        distance = `${distance}m`;
      } else {
        distance = (distance / 1000).toFixed(1);
        distance = `${distance}Km`;
      }
      return distance;
    },
  },
  methods: {
    viewPage(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Nakamal', params: { id } });
        });
    },
    viewMap(id) {
      this.$emit('fly-to-nearby', id);
      // this.$store.dispatch('nakamal/select', id)
      //   .then(() => {
      //     this.$router.push({ name: 'Map' });
      //   });
    },
    kavaSource(ks) {
      let v = ks.province;
      if (ks.island) {
        v += `: ${ks.island}`;
      }
      return v;
    },
  },
  beforeMount() {
    if (!this.hasImages) {
      this.$store.dispatch('image/getNakamal', this.nakamal.id);
    }
  },
};
</script>

<style>

</style>
