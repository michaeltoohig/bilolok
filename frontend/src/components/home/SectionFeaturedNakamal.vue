<template>
  <v-container>
    <h2>
      <v-icon class="pb-2">mdi-trophy-award</v-icon>
      {{ $t('home.featured_nakamal') }}
    </h2>

    <v-container fill-height v-if="nakamal===null">
      <v-layout align-center justify-center>
        <v-flex>
          <div class="text-center">
            <div class="headline my-5">{{ $t('loading.nakamal') }}</div>
            <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container v-else>
      <CardNakamal :nakamal="nakamal" />
    </v-container>
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
      nakamal: null,
    };
  },
  methods: {
    ...mapActions({
      getFeaturedNakamal: 'nakamal/loadFeatured',
    }),
  },
  async mounted() {
    // TODO add cache in vuex store
    this.nakamal = await this.getFeaturedNakamal();
  },
};
</script>

<style>

</style>
