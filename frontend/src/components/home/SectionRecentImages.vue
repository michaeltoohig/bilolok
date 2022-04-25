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
            gradient="
              to bottom,
              rgba(100,115,201,0) 0%,
              rgba(100,115,201,0.1) 75%,
              rgba(25,32,72,.9) 100%
            "
          >
            <div class="d-flex fill-height justify-center align-end text-center">
              <h1>{{ image.nakamal.name }}</h1>
            </div>
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
  beforeMount() {
    this.$store.dispatch('image/getRecent');
  },
};
</script>

<style>

</style>
