<template>
  <v-container v-if="show">
    <h2>Featured Kava Bar</h2>

    <v-container fill-height v-if="nakamal===null">
      <v-layout align-center justify-center>
        <v-flex>
          <div class="text-center">
            <div class="headline my-5">Loading Featured Kava Bar...</div>
            <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <CardNakamal v-else :nakamal="nakamal" />
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import CardNakamal from '@/components/home/CardNakamal.vue';

export default {
  name: 'SectionFeaturedNakamal',
  components: {
    CardNakamal,
  },
  data() {
    return {
      show: true,
    };
  },
  computed: {
    ...mapGetters({
      nakamal: 'nakamal/featured',
    }),
  },
  methods: {
    ...mapActions({
      getFeaturedNakamal: 'nakamal/loadFeatured',
    }),
  },
  async mounted() {
    await this.getFeaturedNakamal();
  },
};
</script>

<style>

</style>
