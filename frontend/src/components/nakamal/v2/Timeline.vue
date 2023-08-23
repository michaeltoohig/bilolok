<template>
  <div>
    <div v-if="isUserVerified">
      <NakamalPost
        :nakamal="nakamal"
        @select-checkin="selectCheckin"
        @select-image="selectImage"
        @select-video="selectVideo"
      ></NakamalPost>

      <hr class="my-3"/>
    </div>

    <v-alert
      v-show="false"
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
import { mapActions, mapGetters } from 'vuex';
import dayjs from 'dayjs';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';
import TripTimelineCard from '@/components/timeline/TripTimelineCard.vue';
import NakamalPost from '@/components/nakamal/NakamalPost.vue';
import nakamalsApi from '@/api/nakamals';

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
      // timelineItems: [],
      // items: [],
    };
  },
  computed: {
    ...mapGetters({
      timelineItems: 'nakamal2/timeline',
      isUserVerified: 'auth/isUserVerified',
      // getImages: 'image/nakamal',
      // getCheckins: 'checkin/nakamal',
      // getVideos: 'video/nakamal',
      // getTrips: 'trip/nakamal',
    }),
    // checkins() {
    //   if (!this.nakamal) return [];
    //   return this.getCheckins(this.nakamal.id);
    // },
    // images() {
    //   if (!this.nakamal) return [];
    //   return this.getImages(this.nakamal.id);
    // },
    // videos() {
    //   if (!this.nakamal) return [];
    //   return this.getVideos(this.nakamal.id);
    // },
    // trips() {
    //   if (!this.nakamal) return [];
    //   return this.getTrips(this.nakamal.id);
    // },
    // timelineItems() {
    //   let items = [];
    //   items = items.concat(this.checkins.map((i) => ({ type: 'checkin', data: i })));
    //   items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
    //   items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
    //   items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
    //   return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    // },
  },
  methods: {
    ...mapActions({
      fetchTimeline: 'nakamal2/fetchTimeline',
    }),
    // async fetchData() {
    //   console.log("fetchData v2 timeline.vue", this.nakamal.id);
    //   const resp = await nakamalsApi.getTimeline(this.nakamal.id);
    //   this.timelineItems = resp.data;
    //   // await Promise.all([
    //   //   this.$store.dispatch('checkin/getNakamal', this.nakamal.id),
    //   //   this.$store.dispatch('image/getNakamal', this.nakamal.id),
    //   //   this.$store.dispatch('trip/getNakamal', this.nakamal.id),
    //   //   this.$store.dispatch('video/getNakamal', this.nakamal.id),
    //   // ]);
    // },
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
    selectImage() {
      this.$emit('select-image');
    },
    selectVideo() {
      this.$emit('select-video');
    },
  },
  async mounted() {
    // TODO rename Timeline
    // fetch timeline API for the nakamal given in props
    // show a loading state while timeline is requested
    // support load more
    // remove dependency on multiple stores
    // this data should update each time checked anyways so don't rely on caching on client (except SW)
    
    // this.loading = true;
    // await this.fetchData();
    await this.fetchTimeline(this.nakamal.id);
    this.loading = false;
  },
};
</script>

<style>

</style>
