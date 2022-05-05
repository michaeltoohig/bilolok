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
        <v-autocomplete
          :items="nakamals"
          :filter="customFilter"
          outlined
          item-value="id"
          item-text="name"
          :label="$t('map.search')"
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

export default {
  name: 'NakamalSearchDialog',
  computed: {
    ...mapGetters({
      showSearch: 'map/showSearch',
      nakamals: 'nakamal/filteredList',
      hasFilters: 'nakamal/hasFilters',
      getNakamalImages: 'image/nakamal',
    }),
  },
  methods: {
    ...mapActions('map', [
      'setShowSearch',
    ]),
    ...mapActions('nakamal', [
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
  },
};
</script>

<style>

</style>
