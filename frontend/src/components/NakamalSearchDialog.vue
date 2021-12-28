<template>
  <v-dialog
    v-model="showSearch"
    persistent
    transition="dialog-bottom-transition"
    max-width="600"
  >
    <v-card>
      <v-toolbar
        color="primary"
        dark
      >
        Search and Filter
      </v-toolbar>
      <v-card-text>
        <v-autocomplete
          :items="nakamals"
          :filter="customFilter"
          outlined
          item-value="id"
          item-text="name"
          label="Search Kava Bars"
          class="mt-3"
          @change="searchSelect"
        >
          <template v-slot:item="data">
            <template>
              <v-list-item-avatar>
                <img
                  v-if="nakamalAvatar(data.item.id)"
                  :src="nakamalAvatar(data.item.id).thumbnail"
                >
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="data.item.name"></v-list-item-title>
                <v-list-item-subtitle
                  v-html="nakamalAliases(data.item.aliases)"
                >
                </v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>
      </v-card-text>
      <v-card-text>
        <v-alert outlined text icon="mdi-map-marker" color="primary" elevation="2">
          {{ nakamals.length }} kava bars on map
        </v-alert>
        <v-select
          @change="changeArea"
          v-model="selectedArea"
          :items="areas"
          item-value="id"
          item-text="name"
          label="Area"
        ></v-select>
        <v-select
          @change="changeLight"
          v-model="selectedLight"
          :items="[
            'White',
            'Red',
            'Orange',
            'Yellow',
            'Green',
            'Blue',
            'Purple',
            'Pink',
            'Other',
          ]"
          label="Light Color"
        ></v-select>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn
          outlined
          @click="clearFilters"
        >
          Clear Filters
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="setShowSearch(false)"
        >
          Close
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import {
  mapActions,
  mapGetters,
} from 'vuex';
import nakamalAreaApi from '@/api/nakamalAreas';

export default {
  name: 'NakamalSearchDialog',
  data() {
    return {
      areas: [],
      selectedArea: null,
      selectedLight: null,
    };
  },
  computed: {
    ...mapGetters({
      showSearch: 'map/showSearch',
      nakamals: 'nakamal/filteredList',
      getNakamalImages: 'image/nakamal',
      filters: 'nakamal/filters',
    }),
  },
  methods: {
    ...mapActions('map', [
      'setShowSearch',
    ]),
    ...mapActions('nakamal', [
      'setFilter',
      'removeFilters',
    ]),
    customFilter(item, queryText) {
      const name = item.name.toLowerCase();
      let aliases = [];
      if (item.aliases) {
        aliases = item.aliases.map((a) => a.toLowerCase());
      }
      const searchText = queryText.toLowerCase();
      return name.indexOf(searchText) > -1 || aliases.some((a) => a.indexOf(searchText) > -1);
    },
    searchSelect(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.setShowSearch(false);
          this.$root.$emit('fly-to-selected');
        });
    },
    nakamalAvatar(nakamalId) {
      const images = this.getNakamalImages(nakamalId);
      if (images.length > 0) {
        return images[0];
      }
      return null;
    },
    nakamalAliases(aliases) {
      if (!aliases) return '-';
      return aliases.join(', ');
    },
    async getAreas() {
      const response = await nakamalAreaApi.getAll();
      this.areas = response.data;
    },
    clearFilters() {
      this.selectedArea = null;
      this.selectedLight = null;
      this.removeFilters();
    },
    changeArea(value) {
      this.setFilter({ key: 'area', value });
    },
    changeLight(value) {
      this.setFilter({ key: 'light', value });
    },
  },
  async beforeMount() {
    await this.getAreas();
  },
  async mounted() {
    if ('area' in this.filters) {
      this.selectedArea = this.filters.area;
    }
    if ('light' in this.filters) {
      this.selectedLight = this.filters.light;
    }
  },
};
</script>

<style>

</style>
