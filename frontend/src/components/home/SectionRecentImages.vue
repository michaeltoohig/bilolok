<template>
  <v-container>
    <h2>Recently Uploaded Images</h2>
    <v-row>
      <v-col cols="12">
        <div v-for="image in images" :key="image.id">
          <CardRecentImage :image="image" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import imagesApi from '@/api/images';
import CardRecentImage from '@/components/home/CardRecentImage.vue';

export default {
  name: 'SectionRecentImages',
  components: {
    CardRecentImage,
  },
  data() {
    return {
      loading: true,
      images: [],
    };
  },
  methods: {
    async getRecentImages() {
      const response = await imagesApi.getRecent();
      this.images = response.data;
    },
  },
  async mounted() {
    await this.getRecentImages();
  },
};
</script>

<style>

</style>
