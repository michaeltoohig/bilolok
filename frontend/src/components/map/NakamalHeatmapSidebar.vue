<template>
  <v-navigation-drawer
    :value="showHeatmapMenu"
    @input="toggleShowHeatmapMenu"
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
        {{ $t('map.heatmap_total_checkins', { count: checkins.length }) }}
      </v-alert>
    </template>

    <v-container>
      <v-switch
        inset
        v-model="toggleHeatmap"
        :label="$t('map.heatmap_show')"
      ></v-switch>

      <v-switch
        v-if="isLoggedIn"
        inset
        v-model="toggleUserOnly"
        :label="$t('map.heatmap_show_only_me')"
        :disabled="!toggleHeatmap"
      ></v-switch>

      <v-switch
        inset
        v-model="toggleDt"
        :label="$t('map.heatmap_show_last_week')"
        :disabled="!toggleHeatmap"
      ></v-switch>
    </v-container>
  </v-navigation-drawer>
</template>

<script>
import dayjs from 'dayjs';
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'NakamalHeatmapSidebar',
  components: {
  },
  data() {
    return {
      toggleHeatmap: false,
      toggleUserOnly: false,
      toggleDt: false,

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
    toggleHeatmap(value) {
      this.setShowHeatmap(value);
    },
    toggleUserOnly(value) {
      if (value) {
        this.changeUser(this.currentUser.id);
      } else {
        this.changeUser(null);
      }
    },
    toggleDt(value) {
      if (value) {
        this.changeDt(dayjs().subtract(7, 'd'));
      } else {
        this.changeDt(null);
      }
    },
  },
  methods: {
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
      this.removeFilters();
    },
    changeUser(user) {
      this.setFilter({ key: 'user', value: user });
    },
    changeDt(dt) {
      this.setFilter({ key: 'dt', value: dt });
    },
  },
  // mounted() {
  //   if (this.showHeatmap) {
  //     this.toggleHeatmap = true;
  //   }
  // },
};
</script>

<style>

</style>
