<template>
  <v-navigation-drawer
    :value="showFilters"
    @input="toggleShowFilters"
    right
    absolute
    temporary
    class="pa-2"
  >
    <template v-slot:prepend>
      <v-alert
        text
        elevation="2"
        icon="mdi-map-marker"
        color="primary"
      >
        {{ nakamals.length }} kava bars on map
      </v-alert>
    </template>
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

    <template v-slot:append>
      <div class="pa-2">
        <v-btn block :disabled="!hasFilters" @click="clearFilters">
          Clear Filters
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import nakamalAreaApi from '@/api/nakamalAreas';

export default {
  name: 'NakamalFilterSidebar',
  data() {
    return {
      areas: [],
      selectedArea: null,
      selectedLight: null,
    };
  },
  computed: {
    ...mapGetters({
      showFilters: 'map/showFilters',
      hasFilters: 'nakamal/hasFilters',
      filters: 'nakamal/filters',
      nakamals: 'nakamal/filteredList',
    }),
  },
  watch: {
    showFilters() {
      // Reset inputs if filters have been removed
      // Does not handle filters being modified in another component
      if (!this.hasFilters) {
        this.selectedArea = null;
        this.selectedLight = null;
      }
    },
  },
  methods: {
    toggleShowFilters(val) {
      // this.setShowFilters(val);
      console.log('yy', val);
    },
    ...mapActions('map', [
      'setShowFilters',
    ]),
    ...mapActions('nakamal', [
      'setFilter',
      'removeFilters',
    ]),
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
};
</script>

<style>

</style>
