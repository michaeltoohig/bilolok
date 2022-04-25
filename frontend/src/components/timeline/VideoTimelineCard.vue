<template>
  <BaseTimelineCard
    :timestamp="item.created_at"
    :user="item.user"
    :nakamal="item.nakamal"
    :linkNakamal="linkNakamal"
  >
    <v-card-text v-if="item.status==='COMPLETE'">
      <video width="100%" :poster="item.cover" controls>
        <source :src="item.src" type="video/webm">
        <p>Sorry, your browser does not support embedded videos. Here is
        a <a :href="item.src">link to the video</a> instead.</p>
      </video>
    </v-card-text>
    <v-card-text v-else-if="item.status!=='ERROR'">
      Your video is still processing and not ready for playing yet.
    </v-card-text>
    <v-card-text v-else>
      Video Error. Something went wrong and we will try to fix it.
      Otherwise we will delete this video in the coming days.
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';

export default {
  name: 'VideoTimelineCard',
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
