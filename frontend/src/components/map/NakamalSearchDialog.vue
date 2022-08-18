<template>
  <v-dialog
    v-model="showSearch"
    persistent
    transition="dialog-bottom-transition"
    max-width="600"
  >
    <v-card>
      <v-card-title>
        {{ $t('map.search') }}
      </v-card-title>
      <v-card-text>
        <InputSearchNakamal :nakamals="nakamals" @on-select="onSelect" />
        <v-alert
          v-if="hasFilters"
          text
          color="secondary"
          elevation="2"
        >
          {{ $t('map.search_filter_alert') }}
        </v-alert>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-spacer></v-spacer>
        <v-btn
          v-if="hasFilters"
          text
          outlined
          @click="removeFilters"
        >
          {{ $t('map.filters_remove') }}
        </v-btn>
        <v-btn
          text
          @click="setShowSearch(false)"
        >
          {{ $t('buttons.close') }}
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
import InputSearchNakamal from '@/components/InputSearchNakamal.vue';

export default {
  name: 'NakamalSearchDialog',
  components: {
    InputSearchNakamal,
  },
  computed: {
    ...mapGetters({
      showSearch: 'map/showSearch',
      nakamals: 'nakamal/filteredList',
      hasFilters: 'nakamal/hasFilters',
    }),
  },
  methods: {
    ...mapActions('map', [
      'setShowSearch',
    ]),
    ...mapActions('nakamal', [
      'removeFilters',
    ]),
    onSelect(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.setShowSearch(false);
          this.$root.$emit('fly-to-selected');
        });
    },
  },
};
</script>

<style>

</style>
