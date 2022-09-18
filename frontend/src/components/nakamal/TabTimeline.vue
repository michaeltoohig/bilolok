<template>
  <div>
    <div v-if="isUserVerified">
      <NakamalPost
        :nakamal="nakamal"
        @select-checkin="selectCheckin"
        @select-video="selectVideo"
      ></NakamalPost>

      <hr class="my-3"/>
    </div>

    <v-alert
      v-show="!checkins.length"
      class="mx-auto elevation-2"
      color="info"
      colored-border
      prominent
      icon="mdi-marker-check"
      border="left"
      max-width="500"
    >
      {{ $t('nakamal.tab_timeline_be_first_to_checkin') }}
    </v-alert>
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">{{ $t('loading.default') }}</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-else>
      <div
        v-for="item in timelineItems"
        :key="item.id"
      >
        <CheckinTimelineCard
          v-if="item.type === 'checkin'"
          :item="item.data"
        />
        <ImageTimelineCard
          v-if="item.type === 'image'"
          :item="item.data"
        />
        <VideoTimelineCard
          v-if="item.type === 'video'"
          :item="item.data"
        />
        <TripTimelineCard
          v-if="item.type === 'trip'"
          :item="item.data"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';
import TripTimelineCard from '@/components/timeline/TripTimelineCard.vue';
import NakamalPost from '@/components/nakamal/NakamalPost.vue';

export default {
  name: 'TabTimeline',
  props: ['nakamal'],
  components: {
    NakamalPost,
    CheckinTimelineCard,
    ImageTimelineCard,
    VideoTimelineCard,
    TripTimelineCard,
  },
  data() {
    return {
      loading: true,
      // items: [],
    };
  },
  computed: {
    ...mapGetters({
      isUserVerified: 'auth/isUserVerified',
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
      getVideos: 'video/nakamal',
      getTrips: 'trip/nakamal',
    }),
    checkins() {
      if (!this.nakamal) return [];
      return this.getCheckins(this.nakamal.id);
    },
    images() {
      if (!this.nakamal) return [];
      return this.getImages(this.nakamal.id);
    },
    videos() {
      if (!this.nakamal) return [];
      return this.getVideos(this.nakamal.id);
    },
    trips() {
      if (!this.nakamal) return [];
      return this.getTrips(this.nakamal.id);
    },
    timelineItems() {
      let items = [];
      items = items.concat(this.checkins.map((i) => ({ type: 'checkin', data: i })));
      items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
      items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
      items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
      return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    },
  },
  methods: {
    async fetchData() {
      await Promise.all([
        this.$store.dispatch('checkin/getNakamal', this.nakamal.id),
        this.$store.dispatch('image/getNakamal', this.nakamal.id),
        this.$store.dispatch('trip/getNakamal', this.nakamal.id),
        this.$store.dispatch('video/getNakamal', this.nakamal.id),
      ]);
    },
    // updateTimelineItems() {
    //   let items = [];
    //   items = items.concat(this.checkins.map((i) => ({ type: 'checkin', data: i })));
    //   items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
    //   items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
    //   items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
    //   return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    // },
    selectCheckin() {
      this.$emit('select-checkin');
    },
    selectVideo() {
      this.$emit('select-video');
    },
  },
  async mounted() {
    this.loading = true;
    // TODO timeline API endpoint instead of this
    await this.fetchData();
    this.loading = false;
  }
  // async mounted() {
  //   this.fetchData();
  // },
};
</script>

<style>

</style>
