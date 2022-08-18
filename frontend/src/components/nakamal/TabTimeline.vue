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
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';
import NakamalPost from '@/components/nakamal/NakamalPost.vue';

export default {
  name: 'TabTimeline',
  props: ['nakamal'],
  components: {
    NakamalPost,
    CheckinTimelineCard,
    ImageTimelineCard,
    VideoTimelineCard,
  },
  computed: {
    ...mapGetters({
      isUserVerified: 'auth/isUserVerified',
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
      getVideos: 'video/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    images() {
      return this.getImages(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    videos() {
      return this.getVideos(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    timelineItems() {
      let items = this.checkins.map((i) => ({ type: 'checkin', data: i }));
      items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
      // items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
      items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
      return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    },
  },
  methods: {
    // async fetchData() {
    //   // TODO fetch data here and show loading for timeline so page can load faster
    //   return null;
    // },
    selectCheckin() {
      this.$emit('select-checkin');
    },
    selectVideo() {
      this.$emit('select-video');
    },
  },
  // async mounted() {
  //   this.fetchData();
  // },
};
</script>

<style>

</style>
