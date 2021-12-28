<template>
  <l-popup
    :options="{ offset: popupOffset }"
    @popupclose="popupClosed"
  >
    <h3 class="mb-2 text-h6 font-weight-bold">{{ selectedNakamal.name }}</h3>
    <v-img
      v-if="selectedNakamalImage"
      contain
      height="114"
      :src="selectedNakamalImage.thumbnail"
    ></v-img>
    <v-list light dense>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">Light</v-list-item-title>
          <v-list-item-subtitle>
            {{ selectedNakamal.light }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold"># of Windows</v-list-item-title>
          <v-list-item-subtitle>
            {{ selectedNakamal.windows || '-' }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">Area</v-list-item-title>
          <v-list-item-subtitle>
            <span v-if="selectedNakamal.area">
              {{ selectedNakamal.area.name }}
            </span>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item>
        <v-list-item-content class="py-0">
          <v-list-item-title class="font-weight-bold">Other Names</v-list-item-title>
          <v-list-item-subtitle>
            {{ aliasNames(selectedNakamal.aliases) }}
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
      View Page
    </v-btn>
  </l-popup>
</template>

<script>
import {
  mapGetters,
} from 'vuex';
import {
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
      selectedNakamal: 'nakamal/selected',
      getNakamalImages: 'image/nakamal',
      getNakamalHasImages: 'image/nakamalHasImages',
    }),
    selectedNakamalImage() {
      if (this.selectedNakamal) {
        if (this.getNakamalHasImages(this.selectedNakamal.id)) {
          return this.getNakamalImages(this.selectedNakamal.id)[0];
        }
      }
      return null;
    },
  },
  methods: {
    popupClosed() {
      this.$store.dispatch('nakamal/unselect');
    },
    aliasNames(aliases) {
      if (!aliases) return '-';
      return aliases.join(', ');
    },
  },
};
</script>

<style>

</style>
