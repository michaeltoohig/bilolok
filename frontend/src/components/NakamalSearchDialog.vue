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
          item-value="id"
          item-text="name"
          label="Kava Bars"
          class="mt-2"
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
      getNakamalImages: 'image/nakamal',
    }),
  },
  methods: {
    ...mapActions('map', [
      'setShowSearch',
    ]),
    customFilter(item, queryText) {
      const name = item.name.toLowerCase();
      const owner = item.owner.toLowerCase();
      const searchText = queryText.toLowerCase();
      return name.indexOf(searchText) > -1 || owner.indexOf(searchText) > -1;
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
  },
};
</script>

<style>

</style>
