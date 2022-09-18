<template>
  <div>
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <!-- TODO loading timeline translation? Or other component for timeline loading -->
              <div class="headline my-5">{{ $t('loading.default') }}</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div
      v-show="!loading && timelineItems.length > 0"
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
    <div v-if="!loading && timelineItems.length === 0">
      <v-alert
        class="mb-3"
        type="warning"
        prominent
        text
      >
        <h3 class="text-h5">
          {{ $t('user.no_activity_title') }}
        </h3>
        <div v-if="isMe">
          {{ $t('user.no_activity_private_body') }}
        </div>
        <div v-else>
          {{ $t('user.no_activity_public_body') }}
        </div>
      </v-alert>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { mapGetters } from 'vuex';

import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import TripTimelineCard from '@/components/timeline/TripTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';

export default {
  name: 'SectionTimeline',
  props: ['userId'],
  components: {
    CheckinTimelineCard,
    ImageTimelineCard,
    TripTimelineCard,
    VideoTimelineCard,
  },
  data() {
    return {
      loading: false,
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      me: 'auth/user',
      getUserCheckins: 'checkin/user',
      getUserImages: 'image/user',
      getUserTrips: 'trip/user',
      getUserVideos: 'video/user',
    }),
    isMe() {
      if (!this.isLoggedIn) return false;
      return this.me.id === this.user.id;
    },
    checkins() {
      return this.getUserCheckins(this.userId);
    },
    images() {
      return this.getUserImages(this.userId);
    },
    trips() {
      return this.getUserTrips(this.userId);
    },
    videos() {
      return this.getUserVideos(this.userId);
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
    // async fetchData() {
    //   await Promise.all([
    //     this.$store.dispatch('checkin/getUser', this.userId),
    //     this.$store.dispatch('image/getUser', this.userId),
    //     this.$store.dispatch('trip/getUser', this.userId),
    //     this.$store.dispatch('video/getUser', this.userId),
    //   ]);
    // },
  },
  // async mounted() {
  //   // TODO timeline API endpoint instead of this
  //   this.loading = true;
  //   // await this.fetchData()
  //   // We need to alert the User view the timeline is ready so that it can stop showing the loading spinner
  //   // And the reason for that is so checkins are loaded into the store which are depended upon by the favorites and cheifOf components
  //   // this.$emits('ready');
  //   this.loading = false;
  // },
};
</script>

<style>

</style>