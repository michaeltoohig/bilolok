<template>
  <v-navigation-drawer
    :value="showFilters"
    @input="toggleShowFilters"
    app
    right
    :temporary="true || $vuetify.breakpoint.mdAndDown"
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
        {{ $t('map.filters_total_nakamals', { count: nakamals.length }) }}
      </v-alert>
    </template>
    <h5>{{ $t('map.filters') }}</h5>
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
      :label="$t('nakamal.attrs.area')"
    ></v-select>
    <v-select
      @change="changeKavaSource"
      v-model="selectedKavaSource"
      :items="kava_sources"
      item-value="id"
      item-text="name"
      :label="$t('nakamal.attrs.kava_source')"
    ></v-select>
    <v-select
      @change="changeResources"
      v-model="selectedResources"
      :items="resources"
      item-value="id"
      item-text="name"
      :label="$t('nakamal.attrs.resources')"
      multiple
    ></v-select>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn block outlined color="primary" :disabled="!hasFilters" @click="clearFilters">
          {{ $t('map.filters_remove') }}
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
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
      const resp = await nakamalAreaApi.getAll();
      this.areas = resp.data;
    },
    async getResources() {
      const resp = await nakamalResourcesApi.getAll();
      this.resources = resp.data;
    },
    async getKavaSources() {
      const resp = await nakamalKavaSourcesApi.getAll();
      this.rawKavaSources = resp.data;
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
      this.$root.$emit('fly-to-bounds');
    },
    changeLight(value) {
      this.setFilter({ key: 'light', value });
      this.$root.$emit('fly-to-bounds');
    },
    changeResources(value) {
      this.setFilter({ key: 'resources', value });
      this.$root.$emit('fly-to-bounds');
    },
    changeKavaSource(value) {
      this.setFilter({ key: 'kava_source', value });
      this.$root.$emit('fly-to-bounds');
    },
  },
  async beforeMount() {
    // TODO move this into the vuex store and when menu is opened then dispatch these
    await this.getAreas();
    await this.getResources();
    await this.getKavaSources();
  },
};
</script>

<style>

</style>
