<template>
  <div>
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
        v-if="getItemType(item) === 'checkin'"
        :item="item"
      />
      <ImageTimelineCard
        v-if="getItemType(item) === 'image'"
        :item="item"
      />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import timeline from '@/mixins/timeline';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';

export default {
  name: 'TabTimeline',
  mixins: [timeline],
  props: ['nakamal'],
  components: {
    CheckinTimelineCard,
    ImageTimelineCard,
  },
  data() {
    return {
      // XXX HACK my `timeline` mixin expects a `trips` and `videos` array.
      trips: [],
      videos: [],
    };
  },
  computed: {
    ...mapGetters({
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    images() {
      return this.getImages(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
  },
};
</script>

<style>

</style>
