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
        Search
      </v-toolbar>
      <v-card-text>
        <v-autocomplete
          :items="nakamals"
          :filter="customFilter"
          outlined
          color="white"
          item-value="id"
          item-text="name"
          label="Kava Bars"
          class="mt-2"
          @change="searchSelect"
        >
          <template v-slot:item="data">
            <template>
              <v-list-item-avatar>
                <img :src="data.item.images.small">
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="data.item.name"></v-list-item-title>
                <v-list-item-subtitle v-html="data.item.owner"></v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>
      </v-card-text>
      <v-card-actions class="justify-end">
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

export default {
  name: 'NakamalSearchDialog',
  computed: {
    ...mapGetters({
      showSearch: 'map/showSearch',
      nakamals: 'nakamal/list',
    }),
  },
  methods: {
    ...mapActions('map', [
      'setShowSearch',
    ]),
    customFilter(item, queryText) {
      const title = item.title.toLowerCase();
      const owner = item.owner.toLowerCase();
      const searchText = queryText.toLowerCase();
      return title.indexOf(searchText) > -1 || owner.indexOf(searchText) > -1;
    },
    searchSelect(id) {
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
