<template>
  <v-navigation-drawer
    :value="showFilters"
    @input="toggleShowFilters"
    app
    right
    :temporary="$vuetify.breakpoint.mdAndDown"
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
    <h5>Filters</h5>
    <SelectLight
      v-model="selectedLight"
      @input="changeLight"
    ></SelectLight>
    <v-select
      @change="changeArea"
      v-model="selectedArea"
      :items="areas"
      item-value="id"
      item-text="name"
      label="Area"
    ></v-select>
    <v-select
      @change="changeKavaSource"
      v-model="selectedKavaSource"
      :items="kava_sources"
      item-value="id"
      item-text="name"
      label="Kava Source"
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
        <v-btn block outlined color="primary" :disabled="!hasFilters" @click="clearFilters">
          Clear Filters
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
// import {
//   latLngBounds,
// } from 'leaflet';
import { mapActions, mapGetters } from 'vuex';
import SelectLight from '@/components/SelectLight.vue';
import nakamalAreaApi from '@/api/nakamalAreas';
import nakamalResourcesApi from '@/api/nakamalResources';
import nakamalKavaSourcesApi from '@/api/nakamalKavaSources';

export default {
  name: 'NakamalFilterSidebar',
  components: {
    SelectLight,
  },
  data() {
    return {
      areas: [],
      selectedArea: null,
      selectedLight: null,
      resources: [],
      selectedResources: [],
      selectedKavaSource: null,
      rawKavaSources: [],
    };
  },
  computed: {
    ...mapGetters({
      showFilters: 'map/showFilters',
      hasFilters: 'nakamal/hasFilters',
      filters: 'nakamal/filters',
      nakamals: 'nakamal/filteredList',
    }),
    kava_sources() {
      /* eslint-disable arrow-body-style */
      return this.rawKavaSources.map((ks) => {
        let name = ks.province;
        if (ks.island) {
          name += `: ${ks.island}`;
        }
        return {
          id: ks.id,
          name,
        };
      }).sort((a, b) => {
        return (a.name < b.name) ? 1 : -1;
      });
    },
  },
  watch: {
    showFilters() {
      // Reset inputs if filters have been removed
      // Does not handle filters being modified in another component
      if (!this.hasFilters) {
        this.selectedArea = null;
        this.selectedLight = null;
        this.selectedKavaSource = null;
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
    async getKavaSources() {
      const response = await nakamalKavaSourcesApi.getAll();
      this.rawKavaSources = response.data;
    },
    clearFilters() {
      this.selectedArea = null;
      this.selectedLight = null;
      this.selectedKavaSource = null;
      this.selectedResources = [];
      this.removeFilters();
    },
    changeArea(value) {
      this.setFilter({ key: 'area', value });
      // const bounds = latLngBounds(this.nakamals.map((n) => n.latLng));
      // this.$store.dispatch('map/setBounds', bounds);
    },
    changeLight(value) {
      this.setFilter({ key: 'light', value });
      // const bounds = latLngBounds(this.nakamals.map((n) => n.latLng));
      // this.$store.dispatch('map/setBounds', bounds);
    },
    changeResources(value) {
      this.setFilter({ key: 'resources', value });
      // const bounds = latLngBounds(this.nakamals.map((n) => n.latLng));
      // this.$store.dispatch('map/setBounds', bounds);
    },
    changeKavaSource(value) {
      this.setFilter({ key: 'kava_source', value });
      // const bounds = latLngBounds(this.nakamals.map((n) => n.latLng));
      // this.$store.dispatch('map/setBounds', bounds);
    },
  },
  async beforeMount() {
    await this.getAreas();
    await this.getResources();
    await this.getKavaSources();
  },
};
</script>

<style>

</style>
