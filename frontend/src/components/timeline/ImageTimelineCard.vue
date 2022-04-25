<template>
  <BaseTimelineCard
    :timestamp="item.created_at"
    :user="item.user"
    :nakamal="item.nakamal"
    :linkNakamal="linkNakamal"
  >
    <v-card-text>
      <v-img
        contain
        :max-height="300"
        :src="item.src"
        :lazy-src="item.msrc"
      ></v-img>
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';

export default {
  name: 'CheckinTimelineCard',
  components: {
    BaseTimelineCard,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>

</style>
