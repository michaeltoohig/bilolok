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
      Be first to check-in!
    </v-alert>
    <div
      v-for="item in timelineItems"
      :key="item.id"
    >
      <CardCheckin v-if="getItemType(item) === 'checkin'" :item="item" :linkUser="true"/>
      <CardImage v-if="getItemType(item) === 'image'" :item="item" :linkUser="true"/>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import timeline from '@/mixins/timeline';
import CardCheckin from '@/components/timeline/CardCheckin.vue';
import CardImage from '@/components/timeline/CardImage.vue';

export default {
  name: 'TabTimeline',
  mixins: [timeline],
  props: ['nakamal'],
  components: {
    CardCheckin,
    CardImage,
  },
  data() {
    return {
      // XXX HACK my `timeline` mixin expects a `trips` array.
      trips: [],
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
