<template>
  <BaseTimelineCard
    :timestamp="item.created_at"
    :user="item.user"
    :nakamal="item.nakamal"
    :linkNakamal="linkNakamal"
  >
    <v-card-text class="d-flex flex-row justify-start align-center">
      <v-icon>mdi-marker-check</v-icon>
      <h2>
        <span>Check-in</span>
      </h2>
    </v-card-text>
    <v-card-text v-if="item.message" class="pt-0 text-h5 font-weight-normal">
      {{ item.message }}
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
