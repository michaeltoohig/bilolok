<template>
  <v-navigation-drawer
    :value="showFilters"
    @input="toggleShowFilters"
    app
    right
    temporary
    touchless
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
    <v-select
      @change="changeResources"
      v-model="selectedResources"
      :items="resources"
      item-value="id"
      item-text="name"
      label="Resources"
      multiple
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
import nakamalResourcesApi from '@/api/nakamalResources';

export default {
  name: 'NakamalFilterSidebar',
  data() {
    return {
      areas: [],
      selectedArea: null,
      selectedLight: null,
      resources: [],
      selectedResources: [],
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
        this.selectedResources = [];
      }
    },
  },
  methods: {
    toggleShowFilters(val) {
      this.setShowFilters(val);
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
    async getResources() {
      const response = await nakamalResourcesApi.getAll();
      this.resources = response.data;
    },
    clearFilters() {
      this.selectedArea = null;
      this.selectedLight = null;
      this.selectedResources = [];
      this.removeFilters();
    },
    changeArea(value) {
      this.setFilter({ key: 'area', value });
    },
    changeLight(value) {
      this.setFilter({ key: 'light', value });
    },
    changeResources(value) {
      this.setFilter({ key: 'resources', value });
    },
  },
  async beforeMount() {
    await this.getAreas();
    await this.getResources();
  },
};
</script>

<style>

</style>
