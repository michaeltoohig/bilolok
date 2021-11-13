<template>
  <v-card>
    <div class="d-flex flex-no-wrap justify-space-between">
      <div>
        <v-card-title
          class="text-h5"
          v-text="nakamal.name"
        ></v-card-title>

        <v-card-actions>
          <v-btn
            class="ml-2 mt-5"
            outlined
            rounded
            small
          >
            View Page
          </v-btn>
        </v-card-actions>
      </div>

      <img
        :src="image.thumbnail"
        :lazy-src="image.msrc"
        aspect-ratio="1"
        class="image ma-3 grey lighten-2"
      />
    </div>
  </v-card>
</template>

<script>
// import { mapGetters } from 'vuex';

export default {
  name: 'CardRecentImage',
  props: ['image'],
  computed: {
    // ...mapGetters({
    //   nakamal: 'nakamal/selected',
    // }),
    nakamal() {
      return this.$store.getters['nakamal/find'](this.image.nakamal_id);
    },
  },
  async mounted() {
    if (!this.nakamal) {
      this.$store.dispatch('nakamal/loadOne', this.image.nakamal_id);
    }
  },
};
</script>

<style>

</style>
