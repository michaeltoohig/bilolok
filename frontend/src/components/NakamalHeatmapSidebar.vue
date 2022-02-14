<template>
  <v-navigation-drawer
    :value="showHeatmapMenu"
    @input="toggleShowHeatmapMenu"
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
        {{ checkins.length }} check-ins on map
      </v-alert>
    </template>

    <v-btn
      block
      :outlined="!showHeatmap"
      @click="toggleShowHeatmap"
      v-text="showHeatmap ? `Hide Heatmap` : `Show Heatmap`"
    ></v-btn>

    <template v-slot:append>
      <div class="pa-2">
        <v-btn
          v-show="false"
          block
          outlined
          color="primary"
          :disabled="!hasFilters"
          @click="clearFilters"
        >
          Clear Filters
        </v-btn>
      </div>
    </template>
  </v-navigation-drawer>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'NakamalHeatmapSidebar',
  components: {
  },
  data() {
    return {
      selectedUser: null,
      showUserCheckins: false,
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      currentUser: 'auth/user',
      showHeatmap: 'map/showHeatmap',
      showHeatmapMenu: 'map/showHeatmapMenu',
      hasFilters: 'checkin/hasFilters',
      filters: 'checkin/filters',
      checkins: 'checkin/filteredList',
    }),
  },
  watch: {
    showHeatmapMenu() {
      // Reset inputs if filters have been removed
      // Does not handle filters being modified in another component
      if (!this.hasFilters) {
        this.showUserCheckins = false;
      }
    },
  },
  methods: {
    toggleShowHeatmap() {
      this.setShowHeatmap(!this.showHeatmap);
    },
    toggleShowHeatmapMenu(val) {
      this.setShowHeatmapMenu(val);
    },
    ...mapActions('map', [
      'setShowHeatmap',
      'setShowHeatmapMenu',
    ]),
    ...mapActions('checkin', [
      'setFilter',
      'removeFilters',
    ]),
    clearFilters() {
      this.user = null;
      this.removeFilters();
    },
    changeUser(value) {
      console.log(333, value, this.currentUser);
      if (value) {
        this.setFilter({ key: 'user', user: this.currentUser.id });
      } else {
        this.clearFilters();
      }
    },
  },
};
</script>

<style>

</style>
