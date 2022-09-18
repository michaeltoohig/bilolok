<template>
  <div class="video">
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">Loading Video...</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-else>
      <v-container class="d-flex justify-center align-center">
        <v-responsive max-width="600" class="pa-3">
          <VideoTimelineCard
            :item="video"
            :linkNakamal="true"
          />
        </v-responsive>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';

export default {
  name: 'Video',
  metaInfo() {
    return {
      // title: undefined,
      // titleTemplate: 'Bilolok - %s',
      meta: [
        // {
        //   property: 'og:title',
        //   content: undefined,
        //   // following template options are identical
        //   // template: '%s - My page',
        //   template: (chunk) => `Bilolok - ${chunk}`,
        //   vmid: 'og:title',
        // },
        {
          property: 'og:image',
          content: this.video ? this.video.cover : undefined,
          vmid: 'og:image',
        },
        {
          property: 'og:image:type',
          content: this.video ? 'image/jpeg' : undefined,
          vmid: 'og:image:type',
        },
        {
          property: 'og:image:width',
          content: this.video ? '480' : undefined,
          vmid: 'og:image:width',
        },
        {
          property: 'og:image:height',
          content: this.video ? '480' : undefined,
          vmid: 'og:image:height',
        },
      ],
    };
  },
  components: {
    VideoTimelineCard,
  },
  data() {
    return {
      loading: true,
    };
  },
  computed: {
    video() {
      const { id } = this.$route.params;
      return this.$store.getters['video/find'](id);
    },
  },
  methods: {
    ...mapActions({
      load: 'video/loadOne',
    }),
  },
  async mounted() {
    this.loading = true;
    const { id } = this.$route.params;
    await this.load(id);
    this.loading = false;
  },
};
</script>

<style>

</style>
