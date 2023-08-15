<template>
  <div>
    <v-container v-if="loading">
      <v-layout align-center justify-center>
        <v-flex>
          <div class="text-center">
            <div class="headline my-5">{{ $t('loading.default') }}</div>
            <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <v-container v-else>
      <h2>{{ $t('home.timeline_title') }}</h2>
      <div
        v-for="item in timelineItems"
        :key="item.data.id"
      >
        <CheckinTimelineCard
          v-if="item.type === 'checkin'"
          :item="item.data"
          :linkNakamal="true"
        />
        <ImageTimelineCard
          v-if="item.type === 'image'"
          :item="item.data"
          :linkNakamal="true"
        />
        <TripTimelineCard
          v-if="item.type === 'trip'"
          :item="item.data"
          :linkNakamal="true"
        />
        <VideoTimelineCard
          v-if="item.type === 'video'"
          :item="item.data"
          :linkNakamal="true"
        />
      </div>
      <div class="text-center">
        <v-icon x-large class="mb-3">mdi-dots-vertical</v-icon>
        <h2 class="headline text-h2">{{ $t('home.end_of_feed') }}</h2>
        <p>{{ $t('home.end_of_feed_extra') }}</p>
        <v-btn
          x-large
          tile
          color="primary"
          :to="{ name: 'Map' }"
        >
          {{ $t('home.go_to_map') }}
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script>
// TODO This component should have a single "timeline" API endpoint to simplify this mess

import dayjs from 'dayjs';
import { mapActions, mapGetters } from 'vuex';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import TripTimelineCard from '@/components/timeline/TripTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';

export default {
  name: 'SectionRecentTimeline',
  components: {
    CheckinTimelineCard,
    ImageTimelineCard,
    TripTimelineCard,
    VideoTimelineCard,
  },
  data() {
    return {
      loading: true,
      recentItemCount: 3,
    };
  },
  computed: {
    ...mapGetters({
      recentCheckins: 'checkin/recent',
      recentImages: 'image/recent',
      recentTrips: 'trip/recent',
      recentVideos: 'video/recent',
    }),
    checkins() {
      // const n = Math.min(this.recentCheckins.length, this.recentItemCount);
      return this.recentCheckins; //.slice(0, n);
    },
    images() {
      // const n = Math.min(this.recentImages.length, this.recentItemCount);
      return this.recentImages; //.slice(0, n);
    },
    trips() {
      // const n = Math.min(this.recentImages.length, this.recentItemCount);
      return this.recentTrips; //.slice(0, n);
    },
    videos() {
      // const n = Math.min(this.recentVideos.length, this.recentItemCount);
      return this.recentVideos; //.slice(0, n);
    },
    timelineItems() {
      let items = this.checkins.map((i) => ({ type: 'checkin', data: i }));
      items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
      items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
      items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
      return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    },
  },
  methods: {
    ...mapActions({
      getRecentCheckins: 'checkin/getRecent',
      getRecentImages: 'image/getRecent',
      getRecentTrips: 'trip/getRecent',
      getRecentVideos: 'video/getRecent',
    }),
    async fetchData() {
      this.loading = true;
      await this.getRecentCheckins();
      await this.getRecentImages();
      await this.getRecentTrips();
      await this.getRecentVideos();
      this.loading = false;
    },
  },
  async mounted() {
    await this.fetchData();
  },
};
</script>

<style>

</style>
