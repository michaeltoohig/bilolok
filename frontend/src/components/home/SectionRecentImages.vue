<template>
  <v-container>
    <h2>Recently Uploaded Images</h2>
    <v-row>
      <v-col cols="12">
        <v-carousel
          hide-delimiters
        >
          <v-carousel-item
            :to="{ name: 'Nakamal', params: { id: image.nakamal.id } }"
            v-for="(image,i) in images"
            :key="i"
            :src="image.src"
            :lazy-src="image.msrc"
          >
          </v-carousel-item>
        </v-carousel>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'SectionRecentImages',
  components: {
  },
  data() {
    return {
    };
  },
  computed: {
    ...mapGetters({
      images: 'image/recent',
    }),
  },
  methods: {
    // async getRecentImages() {
    //   const response = await imagesApi.getRecent();
    //   this.images = response.data;
    // },
  },
  beforeMount() {
    this.$store.dispatch('image/getRecent');
  },
};
</script>

<style>

</style>
