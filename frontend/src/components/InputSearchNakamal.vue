<template>
  <v-autocomplete
    :items="nakamals"
    :filter="customFilter"
    outlined
    item-value="id"
    item-text="name"
    prepend-icon="mdi-magnify"
    :label="$t('map.search')"
    class="mt-3"
    @change="onSelect"
  >
    <template v-slot:item="data">
      <template>
        <v-badge
          v-if="nakamalAvatar(data.item.id)"
          :color="data.item.lightBadge.color"
          dot
          overlap
          bordered
          left
          offset-x="24"
          offset-y="18"
          dark
        >
          <v-list-item-avatar>
            <img
              :src="nakamalAvatar(data.item.id).thumbnail"
            >
          </v-list-item-avatar>
        </v-badge>
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
</template>

<script>
import {
  mapActions,
  mapGetters,
} from 'vuex';

export default {
  name: 'InputSearchNakamal',
  emits: ['on-select'],
  props: ['nakamals'],
  computed: {
    ...mapGetters({
      getNakamalImages: 'image/nakamal',
    }),
  },
  methods: {
    onSelect(id) {
      this.$emit('on-select', id);
    },
    customFilter(item, queryText) {
      const name = item.name.toLowerCase();
      let aliases = [];
      if (item.aliases) {
        aliases = item.aliases.map((a) => a.toLowerCase());
      }
      const searchText = queryText.toLowerCase();
      return name.indexOf(searchText) > -1 || aliases.some((a) => a.indexOf(searchText) > -1);
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
