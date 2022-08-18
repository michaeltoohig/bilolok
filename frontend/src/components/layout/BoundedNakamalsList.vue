<template>
  <v-virtual-scroll
    :items="boundNakamals"
    :item-height="50"
    height="300px"
  >
    <template v-slot:default="{ item }">
      <v-list-item
        :key="item.id"
        @click="select(item.id)"
      >
        <v-list-item-icon v-if="item.id === selectedNakamal">
          <v-icon>mdi-star</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{ item.name }}</v-list-item-title>
      </v-list-item>
    </template>
  </v-virtual-scroll>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'BoundedNakamals',
  computed: {
    ...mapGetters({
      bounds: 'map/bounds',
      nakamals: 'nakamal/filteredList',
      selectedNakamal: 'nakamal/selected',
    }),
    boundNakamals() {
      if (!this.bounds) return [];
      return this.nakamals.filter((n) => this.bounds.contains(n.latLng));
    },
  },
  methods: {
    select(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$emit('close-drawer');
          this.$root.$emit('fly-to-selected');
        });
    },
  },
};
</script>

<style>

</style>
